(ns pages.predictions
  (:require [reagent.core :as r]
            [app.state :refer [app-state]]))

(defn ^:private add-project-modal []
  (let [p-name (r/atom "")
        p-descr (r/atom "")]
    (fn []
  [:div
    [:div {:class "modal fade" :id "addProjModal" :tabIndex "-1" :role "dialog"
           :aria-labelledby "addProjectModalLabel"}
      [:div {:class "modal-dialog" :role "document"}
        [:div {:class "modal-content"}
          [:div {:class "modal-header"}
            [:button {:type "button" :class "close"
                      :data-dismiss "modal" :aria-label "Close"}
              [:span {:aria-hidden "true"} "x"]]
            [:h4 {:class "modal-title" :id "addProjectModalLabel"}
              "Create a new project"]]
          [:div {:class "modal-body"}
            [:div {:class "form-horizontal"}
              [:div {:class "form-group"}
                [:label {:class "control-label col-sm-3" :for "nameInput"}
                  "Project name*"]
                [:div {:class "col-sm-9"}
                  [:input {:type "text" :class "form-control"
                           :on-change #(reset! p-name (-> % .-target .-value))
                           :value @p-name :id "nameInput"
                           :placeholder "Project name"}]]]
             [:div {:class "form-group"}
               [:label {:class "control-label col-sm-3" :for "descrInput"}
                 "Description"]
               [:div {:class "col-sm-9"}
                 [:input {:type "text" :class "form-control"
                          :on-change #(reset! p-descr (-> % .-target .-value))
                          :value @p-descr :id "descrInput"
                          :placeholder "Project description"}]]]]]
          [:div {:class "modal-footer"}
            [:button {:type "button" :class "btn btn-default"
                      :data-dismiss "modal"} "Close"]
            [:button {:type "button" :class "btn btn-primary"
                      :data-dismiss "modal"
                      :on-click #(do nil)}
              "Create"]]]]]
    [:button {:type "button" :class "btn btn-primary"
              :data-toggle "modal" :data-target "#addProjModal"}
      "New Simulation"]])))

(defn component []
  (let [refreshing (r/atom false)]
    (fn []
    [:div {:class "container"} [:h1 {:class "page-header"} "Make a bet ;)"]
      [:div {:class "btn-toolbar" :role "toolbar"}
        [add-project-modal]]])))
