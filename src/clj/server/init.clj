(ns server.init
  (:require [stats.players :as players]))

(defn init!
  "Load data"
  []
  (players/init!))
