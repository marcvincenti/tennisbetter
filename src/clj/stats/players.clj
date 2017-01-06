(ns stats.players
  (:require [ring.util.response :refer [response]]
            [clojure.data.csv :as csv]
            [clojure.java.io :as io]
            [clj-time.format :as f]))

(def ^:private date-formatter (f/formatter "dd/MM/yyyy"))
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
      (swap! players update-in [(keyword winner)] conj {:date  date
                                                        :surface surface
                                                        :win true
                                                        :opponent looser})
      (swap! players update-in [(keyword looser)] conj {:date  date
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
