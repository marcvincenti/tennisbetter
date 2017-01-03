(ns pages.about
  (:require [app.state :refer [app-state]]))

(defn component []
  [:div {:class "container"}
    [:h1 {:class "page-header"} "@app-state"]
    [:p (str @app-state)]])
