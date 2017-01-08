(ns providers.data
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [app.state :refer [app-state]]))

(defn load-players
  "Load players list from the server"
  []
  (go (let [token (get @app-state :session)
            response (<! (http/get "/api/players"
                          {:query-params {:token token}}))]
    (when (:success response)
      (swap! app-state assoc :players
        (into (sorted-map)
          (reduce #(assoc %1 (keyword (:id %2)) %2) {}
            (get-in response [:body :players]))))))))
