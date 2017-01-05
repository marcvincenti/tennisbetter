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
  (go (let [params (merge {:token (:session @app-state)} (:form-p @app-state))
            response (<! (http/get "/api/prediction"
                          {:query-params params}))]
    (if (:success response)
      (.log js/console (get-in response [:body :prediction]))
      (reset! isError true))
    (reset! isLoading false))))
