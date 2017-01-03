(ns providers.auth
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [reagent.core :as r]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [app.state :refer [app-state]]
            [providers.cookies :as cookies]))

(defn retrieve-session
  "Retry to connect from an od session stored in cookies"
  []
  (let [token (cookies/get :session)]
    (when token
      (go (let [response (<! (http/get "/api/test-token"
                              {:query-params {:token token}}))]
        (when (:success response)
          (swap! app-state assoc :session
            (get-in response [:body :token]))))))))

(defn login
  "Log a user with a specific password defined in the cloud"
  [password remember loading error]
  (reset! loading true)
  (go (let [response (<! (http/post "/api/login"
                        {:form-params {:password @password}}))]
    (if (:success response)
      ;login success
      (do
        (swap! app-state assoc :page :predictions
                               :session (get-in response [:body :token]))
        (when remember (cookies/set :session (get-in response [:body :token]))))
      ;login failed
      (do (reset! password "")
        (reset! error true)))
    (reset! loading false))))

(defn logout
  "Log the user out"
  []
  (do
    (cookies/remove :session)
    (http/post "/api/logout" {:form-params {:token (:session @app-state)}})
    (swap! app-state dissoc :session)))
