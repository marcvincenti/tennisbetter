(ns server.handler
  (:require [ring.middleware.json :refer [wrap-json-response]]
            [ring.middleware.multipart-params :refer [wrap-multipart-params]]
            [ring.middleware.keyword-params :refer [wrap-keyword-params]]
            [ring.middleware.params :refer [wrap-params]]
            [server.routes :as routes]))

(def app (->  routes/app
              wrap-keyword-params
              wrap-params
              wrap-json-response ))
