(ns pages.predictions
  (:require [reagent.core :as r]
            [providers.data :as data]
            [components.datepicker :as dt]
            [app.state :refer [app-state]]))

(defn component []
  (let [refreshing (r/atom false)]
    (when empty? (get @app-state :players) (data/load-players))
    (fn []
    [:div {:class "container"} [:h1 {:class "page-header"} "Make a bet ;)"]

      [:div {:class "panel panel-default"}
        [:div {:class "panel-heading"} "Complete match profile"]
        [:div {:class "panel-body"}

          [:div {:class "form-group"}
            [:label {:for "player1"} "Select a player"]
            [:select {:class "form-control" :id "player1"}
              (for [p (get @app-state :players)] ^{:key p} [:option p])]]
          [:div {:class "form-group"}
            [:label {:for "rank1"} "Rank"]
            [:input {:class "form-control" :type "number" :id "rank1"}]]
          [:div {:class "form-group"}
            [:label {:for "points1"} "Points"]
            [:input {:class "form-control" :type "number" :id "points1"}]]
          [:div {:class "form-group"}
            [:label {:for "odds1"} "Odds"]
            [:input {:class "form-control" :type "number" :id "odds1"}]]

          [:div {:class "form-group"}
            [:label {:for "player2"} "Select opponent"]
            [:select {:class "form-control" :id "player2"}
              (for [p (get @app-state :players)] ^{:key p} [:option p])]]
          [:div {:class "form-group"}
            [:label {:for "rank2"} "Rank"]
            [:input {:class "form-control" :type "number" :id "rank2"}]]
          [:div {:class "form-group"}
            [:label {:for "points2"} "Points"]
            [:input {:class "form-control" :type "number" :id "points2"}]]
          [:div {:class "form-group"}
            [:label {:for "odds2"} "Odds"]
            [:input {:class "form-control" :type "number" :id "odds2"}]]

          [:div {:class "form-group"}
            [:label {:for "date"} "Date"]
            [dt/datepicker]]

        ]]])))
