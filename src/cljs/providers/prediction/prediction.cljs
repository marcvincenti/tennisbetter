(ns providers.prediction
  (:refer-clojure :exclude [get])
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [app.state :refer [app-state]]))

(defn get
  "Return a prediction"
  [isLoading isError]
  (reset! isLoading true)
  (go (let [token (get @app-state :session)
            response (<! (http/get "/api/prediction"
                          {:query-params {:token token}}))]
    (if (get response :success)
      (.log js/console "YOUPII!")
      (reset! isError true))
    (reset! isLoading false))))
