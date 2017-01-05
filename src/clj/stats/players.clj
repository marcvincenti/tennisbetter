(ns stats.players
  (:require [ring.util.response :refer [response]]
            [utils :as util]
            [clojure.set :refer [intersection]]
            [clojure.data.csv :as csv]
            [clojure.java.io :as io]
            [clj-time.format :as f]))

(def ^:private date-formatter (f/formatter "dd/MM/yyyy"))
(def ^:private matches-files ["resources/private/mens.csv"])
(def ^:private players (atom {}))

(defn ^:private load-results
  "load matches results in players"
  [match]
  (let [winner (get match 9)
        looser (get match 10)
        surface (get match 6)
        date (f/parse date-formatter (get match 3))]
    (do
      (swap! players update-in [(keyword winner)] conj {:date  date
                                                        :surface surface
                                                        :win true
                                                        :opponent looser})
      (swap! players update-in [(keyword winner)] conj {:date  date
                                                        :surface surface
                                                        :win false
                                                        :opponent winner}))))

(defn ^:private read-csv
  "Read a csv and store matches results"
  [file-name]
  (with-open [in-file (io/reader file-name)]
    (let [m (csv/read-csv in-file)]
      (run! load-results m))))

(defn init!
  "Load players data from matches-files"
  []
  (run! read-csv matches-files))

(defn get!
  "Return a list of all the Players"
  [& args]
  (response {:players (keys @players)}))

(defn ^:private ratio
  "Return ratio between 2 int"
  [int1 int2]
  (if-not (and (zero? int2) (zero? int1))
    (double (/ int1 (+ int1 int2)))
    0))

(defn ^:private opponent-model-inc
  [matches player-list surface win-all win-surface loose-all loose-surface]
  (run!
    (fn [m] (when (contains? player-list (:opponent m))
      (if (:win m)
        (do ;did win
          (swap! win-all inc)
          (when (= surface (:surface m))
            (swap! win-surface inc)))
        (do ;did loose
          (swap! loose-all inc)
          (when (= surface (:surface m))
            (swap! loose-surface inc))))))
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
        p1-matches ((keyword player1) @players)
        p2-matches ((keyword player2) @players)
        p1-opponents (reduce #(conj %1 (:opponent %2)) #{} p1-matches)
        p2-opponents (reduce #(conj %1 (:opponent %2)) #{} p2-matches)
        p1-p2-opps (intersection p1-opponents p2-opponents)]
    (do
      (opponent-model-inc p1-matches p1-p2-opps surface
        p1-win-all-surfaces p1-win-this-surface
        p1-loose-all-surfaces p1-loose-this-surface)
      (opponent-model-inc p2-matches p1-p2-opps surface
        p2-win-all-surfaces p2-win-this-surface
        p2-loose-all-surfaces p2-loose-this-surface)
      [(- (ratio @p1-win-all-surfaces @p1-loose-all-surfaces)
              (ratio @p2-win-all-surfaces @p2-loose-all-surfaces))
            (- (ratio @p1-win-this-surface @p1-loose-this-surface)
               (ratio @p2-win-this-surface @p2-loose-this-surface))])))

(defn predict
  "Return a multiplier to bet the match"
  [{:keys [player1 player2 rank1 rank2 points1
           points2 odds1 odds2 surface date]}]
  (prn (concat [(- (util/str->int rank1) (util/str->int rank2))
         (- (util/str->int points1) (util/str->int points2))]
        (opponent-model player1 player2 surface)))
  (response {:prediction (rand)}))
