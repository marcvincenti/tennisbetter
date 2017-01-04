(ns providers.data
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [app.state :refer [app-state]]))

(defn load-players
  "Load players list from the server"
  []
  (go (let [response (<! (http/get "/api/players"))]
    (when (:success response)
      (swap! app-state assoc :players
        (get-in response [:body :players]))))))
