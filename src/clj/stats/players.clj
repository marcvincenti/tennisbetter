(ns stats.players
  (:require [ring.util.response :refer [response]]
            [clojure.data.csv :as csv]
            [clojure.java.io :as io]))

(def ^:private matches-files ["resources/private/mens.csv"])
(def ^:private players (atom {}))

(defn ^:private load-results
  "load matches results in players"
  [match]
  (let [winner (get match 9)
        looser (get match 10)
        surface (get match 6)
        timestamp (get match 3)]
  (swap! players assoc (keyword winner) 0
                       (keyword looser) 0)))

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

(defn predict
  "Return a multiplier to bet the match"
  [{:keys []}]
  (response {:prediction (rand)}))
