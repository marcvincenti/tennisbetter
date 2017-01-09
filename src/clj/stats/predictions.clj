(ns stats.predictions
  (:require [ring.util.response :refer [response]]
            [amazonica.aws.machinelearning :as ml :only [predict]]
            [utils :as util]
            [clojure.set :refer [intersection]]
            [stats.players :refer [players]]
            [clj-time.format :as f]
            [clj-time.core :as t]))

(def ^:private date-formatter (f/formatter "dd/MM/yyyy"))
(def ^:private ml-model-id (System/getenv "ML_MODEL_ID"))
(def ^:private ml-model-endpoint (System/getenv "ML_MODEL_ENDPOINT"))

(defn ^:private ratio
  "Return ratio between 2 int"
  [int1 int2]
  (if-not (zero? int2)
    (double (/ int1 (+ int1 int2)))
    0))

(defn ^:private match-inc
  [match surface win-all loose-all win-surface loose-surface]
  (if (:win match)
    (do ;did win
      (swap! win-all inc)
      (when (= surface (:surface match))
        (swap! win-surface inc)))
    (do ;did loose
      (swap! loose-all inc)
      (when (= surface (:surface match))
        (swap! loose-surface inc)))))

(defn ^:private opponent-model-inc
  [matches player-list surface win-all loose-all win-surface loose-surface]
  (run!
    (fn [m] (when (contains? player-list (:opponent m))
      (match-inc m surface win-all loose-all win-surface loose-surface)))
  matches))

(defn ^:private opponent-model
  "Knottenbelt’s Common-Opponent model simplified"
  [player1 player2 surface]
  (let [p1-win-all-surfaces (atom 0)
        p1-win-this-surface (atom 0)
        p1-loose-all-surfaces (atom 0)
        p1-loose-this-surface (atom 0)
        p2-win-all-surfaces (atom 0)
        p2-win-this-surface (atom 0)
        p2-loose-all-surfaces (atom 0)
        p2-loose-this-surface (atom 0)
        p1-matches (:m ((keyword player1) @players))
        p2-matches (:m ((keyword player2) @players))
        p1-opponents (reduce #(conj %1 (:opponent %2)) #{} p1-matches)
        p2-opponents (reduce #(conj %1 (:opponent %2)) #{} p2-matches)
        p1-p2-opps (intersection p1-opponents p2-opponents)]
    (do
      (opponent-model-inc p1-matches p1-p2-opps surface
        p1-win-all-surfaces p1-loose-all-surfaces
        p1-win-this-surface p1-loose-this-surface)
      (opponent-model-inc p2-matches p1-p2-opps surface
        p2-win-all-surfaces p2-loose-all-surfaces
        p2-win-this-surface p2-loose-this-surface)
      (let [diff-all (- (ratio @p1-win-all-surfaces @p1-loose-all-surfaces)
                      (ratio @p2-win-all-surfaces @p2-loose-all-surfaces))
            diff-surface (- (ratio @p1-win-this-surface @p1-loose-this-surface)
                          (ratio @p2-win-this-surface @p2-loose-this-surface))]
        {"Var03" diff-all "Var04" diff-surface}))))

(defn ^:private historical-model-inc
 [matches surface date win-all-6 loose-all-6 win-all-12 loose-all-12
 win-all-18 loose-all-18 win-surface-6 loose-surface-6 win-surface-12
 loose-surface-12 win-surface-18 loose-surface-18]
 (let [fdate (f/parse date-formatter date)
       six-months-ago (t/minus fdate (t/months 6))
       twelve-months-ago (t/minus fdate (t/years 1))
       eighteen-months-ago (t/minus fdate (t/months 18))]
   (run!
     (fn [m] (cond
       (t/within? (t/interval eighteen-months-ago twelve-months-ago) (:date m))
        (match-inc m surface win-all-18 loose-all-18
                             win-surface-18 loose-surface-18)
       (t/within? (t/interval twelve-months-ago six-months-ago) (:date m))
        (match-inc m surface win-all-12 loose-all-12
                             win-surface-12 loose-surface-12)
       (t/within? (t/interval six-months-ago fdate) (:date m))
         (match-inc m surface win-all-6 loose-all-6
                              win-surface-6 loose-surface-6)))
    matches)))

(defn ^:private historical-model
 "Our own Historical-Opponent model"
 [player1 player2 surface date]
 (let [p1-win-all-6months (atom 0) p1-loose-all-6months (atom 0)
       p1-win-all-12months (atom 0) p1-loose-all-12months (atom 0)
       p1-win-all-18months (atom 0) p1-loose-all-18months (atom 0)
       p1-win-surface-6months (atom 0) p1-loose-surface-6months (atom 0)
       p1-win-surface-12months (atom 0) p1-loose-surface-12months (atom 0)
       p1-win-surface-18months (atom 0) p1-loose-surface-18months (atom 0)
       p2-win-all-6months (atom 0) p2-loose-all-6months (atom 0)
       p2-win-all-12months (atom 0) p2-loose-all-12months (atom 0)
       p2-win-all-18months (atom 0) p2-loose-all-18months (atom 0)
       p2-win-surface-6months (atom 0) p2-loose-surface-6months (atom 0)
       p2-win-surface-12months (atom 0) p2-loose-surface-12months (atom 0)
       p2-win-surface-18months (atom 0) p2-loose-surface-18months (atom 0)
       p1-matches (:m ((keyword player1) @players))
       p2-matches (:m ((keyword player2) @players))]
   (do
     (historical-model-inc p1-matches     surface   date
                           p1-win-all-6months       p1-loose-all-6months
                           p1-win-all-12months      p1-loose-all-12months
                           p1-win-all-18months      p1-loose-all-18months
                           p1-win-surface-6months   p1-loose-surface-6months
                           p1-win-surface-12months  p1-loose-surface-12months
                           p1-win-surface-18months  p1-loose-surface-18months)
     (historical-model-inc p2-matches     surface   date
                           p2-win-all-6months       p2-loose-all-6months
                           p2-win-all-12months      p2-loose-all-12months
                           p2-win-all-18months      p2-loose-all-18months
                           p2-win-surface-6months   p2-loose-surface-6months
                           p2-win-surface-12months  p2-loose-surface-12months
                           p2-win-surface-18months  p2-loose-surface-18months)
     (let [diff-all-6 (- (ratio @p1-win-all-6months  @p1-loose-all-6months)
                        (ratio @p2-win-all-6months  @p2-loose-all-6months))
      diff-all-12 (- (ratio @p1-win-all-12months  @p1-loose-all-12months)
                    (ratio @p2-win-all-12months  @p2-loose-all-12months))
      diff-all-18 (- (ratio @p1-win-all-18months  @p1-loose-all-18months)
                    (ratio @p2-win-all-18months  @p2-loose-all-18months))
      diff-s-6 (- (ratio @p1-win-surface-6months  @p1-loose-surface-6months)
                (ratio @p2-win-surface-6months  @p2-loose-surface-6months))
      diff-s-12 (- (ratio @p1-win-surface-12months  @p1-loose-surface-12months)
                  (ratio @p2-win-surface-12months  @p2-loose-surface-12months))
      diff-s-18 (- (ratio @p1-win-surface-18months  @p1-loose-surface-18months)
                  (ratio @p2-win-surface-18months  @p2-loose-surface-18months))]
       {"Var05" diff-all-6 "Var06" diff-all-12 "Var07" diff-all-18
         "Var08" diff-s-6 "Var09" diff-s-12 "Var10" diff-s-18}))))

(defn predict
  "Return a multiplier to bet the match"
  [{:keys [player1 player2 rank1 rank2 points1
           points2 odds1 odds2 surface date]}]
  (let [records (merge {"Var01" (- (util/str->int rank1) (util/str->int rank2))
                    "Var02" (- (util/str->int points1) (util/str->int points2))}
                    (opponent-model player1 player2 surface)
                    (historical-model player1 player2 surface date))
        pred (ml/predict {:MLModelId ml-model-id :record records
                          :predict-endpoint ml-model-endpoint})
        static-amount 20
        score-model (first (vals (get-in pred [:prediction :predicted-scores])))
        oddJ1 (util/str->float odds1)
        oddJ2 (util/str->float odds2)
        score-market (ratio oddJ2 oddJ1)
        kelly (if (> score-model score-market)
                (/ (* static-amount (- (* score-model (+ 1 (double (/ oddJ2 oddJ1)))) 1) oddJ2)) 0)]
    (response {:kelly kelly})))
