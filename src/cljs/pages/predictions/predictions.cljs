(ns pages.predictions
  (:require [reagent.core :as r]
            [providers.data :as data]
            [providers.prediction :as prediction]
            [components.alerts :as alerts]
            [components.datepicker :as dt]
            [app.state :refer [app-state]]))

(defn component []
  (let [loading? (r/atom false)
        error? (r/atom false)]
    (when (empty? (get @app-state :players)) (data/load-players))
    (fn []
      [:div {:class "container"} [:h1 {:class "page-header"} "Make a bet ;)"]

        [:div {:class "panel panel-default"}
          [:div {:class "panel-heading"} "Complete match profile"]
          [:div {:class "panel-body"}
            (alerts/danger error?
              "An error occured. Have you filled the fields correctly ?")
            ;Player1
            [:div {:class "form-group"}
              [:label {:for "player1"} "Select a player"]
              [:select {:class "form-control" :id "player1"
                        :on-change #(swap! app-state assoc-in [:form-p :player1]
                                    (-> % .-target .-value))
                        :value (or (get-in @app-state [:form-p :player1]) "")}
                [:option ""]
                (for [p (get @app-state :players)] ^{:key p} [:option (:id p)])]]
            [:div {:class "form-group"}
              [:label {:for "rank1"} "Rank"]
              [:input {:class "form-control" :type "number" :id "rank1"
                       :on-change #(swap! app-state assoc-in [:form-p :rank1]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :rank1])}]]
            [:div {:class "form-group"}
              [:label {:for "points1"} "Points"]
              [:input {:class "form-control" :type "number" :id "points1"
                       :on-change #(swap! app-state assoc-in [:form-p :points1]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :points1])}]]
            [:div {:class "form-group"}
              [:label {:for "odds1"} "Odds"]
              [:input {:class "form-control" :type "number" :id "odds1"
                       :on-change #(swap! app-state assoc-in [:form-p :odds1]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :odds1])}]]
            ;Player2
            [:div {:class "form-group"}
              [:label {:for "player2"} "Select opponent"]
              [:select {:class "form-control" :id "player2"
                        :on-change #(swap! app-state assoc-in [:form-p :player2]
                                    (-> % .-target .-value))
                        :value (or (get-in @app-state [:form-p :player2]) "")}
                [:option ""]
                (for [p (get @app-state :players)] ^{:key p} [:option (:id p)])]]
            [:div {:class "form-group"}
              [:label {:for "rank2"} "Rank"]
              [:input {:class "form-control" :type "number" :id "rank2"
                       :on-change #(swap! app-state assoc-in [:form-p :rank2]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :rank2])}]]
            [:div {:class "form-group"}
              [:label {:for "points2"} "Points"]
              [:input {:class "form-control" :type "number" :id "points2"
                       :on-change #(swap! app-state assoc-in [:form-p :points2]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :points2])}]]
            [:div {:class "form-group"}
              [:label {:for "odds2"} "Odds"]
              [:input {:class "form-control" :type "number" :id "odds2"
                       :on-change #(swap! app-state assoc-in [:form-p :odds2]
                                  (-> % .-target .-value))
                       :value (get-in @app-state [:form-p :odds2])}]]
            ;Match Data
            [:div {:class "form-group"}
              [:label {:for "surface"} "Surface"]
              [:select {:class "form-control" :id "surface"
                        :on-change #(swap! app-state assoc-in [:form-p :surface]
                                    (-> % .-target .-value))
                        :value (or (get-in @app-state [:form-p :surface]) "")}
                [:option ""][:option "Hard"][:option "Clay"][:option "Grass"]]]
            [:div {:class "form-group"}
              [:label {:for "date"} "Date"]
              [dt/datepicker]]

            [:div {:class "form-group"}
              [:button {:on-click #(prediction/get loading? error?)
                        :type "button"
                        :class (str "btn btn-success btn-block"
                          (when @loading? " disabled"))}
                (if @loading? "Loading..." "Prediction")]]]]])))
