(ns stats.players
  (:require [ring.util.response :refer [response]]
            [net.cgrand.enlive-html :as html]
            [clojure.data.csv :as csv]
            [clojure.java.io :as io]
            [utils :as util]
            [clj-time.format :as f]))

(def ^:private date-formatter (f/formatter "dd/MM/yyyy"))
(def ^:private link-ranks "http://live-tennis.eu/fr/classement-atp-officiel")
(def ^:private matches-files ["resources/private/mens.csv"])

(def players (atom {}))

(defn ^:private load-results
  "load matches results in players"
  [match]
  (let [winner (get match 9)
        looser (get match 10)
        surface (get match 6)
        date (f/parse date-formatter (get match 3))]
    (do
      (swap! players update-in [(keyword winner) :m] conj {:date  date
                                                           :surface surface
                                                           :win true
                                                           :opponent looser})
      (swap! players update-in [(keyword looser) :m] conj {:date  date
                                                           :surface surface
                                                           :win false
                                                           :opponent winner}))))

(defn ^:private read-csv
  "Read a csv and store matches results"
  [file-name]
  (with-open [in-file (io/reader file-name)]
    (let [m (csv/read-csv in-file)]
      (run! load-results m))))

(defn ^:private load-ranks
  "Load ranks and points from the internet"
  []
  (let [page (html/html-resource (java.net.URL. link-ranks))
        p (rest (html/select page [:table#t868 :> [:tr (html/attr? :bgcolor :class)]]))
        mapper (fn [row]
                (let [content (:content row)
                      rank (util/str->int (subs (first (:content (nth content 0))) 1))
                      name (first (:content (nth content 2)))
                      points (util/str->int (first (:content (nth content 5))))]
                  {:name name :rank rank :points points}))
        info-players (map mapper p)]
    (run! (fn [player]
       (let [name (name player)
             f-name (first (get (re-find #"^* ([\w-.]+).$" name) 1))
             l-name (clojure.string/replace
                      (or (get (re-find #"^([\w- ]+) [\w-.]+.$" name) 1) "")
                      #"-" " ")
             regex (str "^" f-name "[\\w ]+ " l-name "$")]
        (run! #(let [match-expr (re-find (re-pattern regex) (:name %))]
                (when-not (empty? match-expr)
                  (swap! players update player conj %)))
          info-players)))
      (keys @players))))

(defn init!
  "Load players data from matches-files"
  []
  (do
    (run! read-csv matches-files)
    (load-ranks)))

(defn get!
  "Return a list of all the Players"
  [& args]
  (response {:players
    (reduce-kv
      (fn [m k v]
        (conj m (merge {:id (name k)}
                      (select-keys v [:name :rank :points]))))
      [] @players)}))
