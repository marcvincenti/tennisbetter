(ns pages.login
  (:require [reagent.core :as r]
            [app.state :refer [app-state]]
            [components.alerts :as alerts]
            [providers.auth :as auth]))

(defn ^:private login-form []
  (let [remember-me? (r/atom true)
        password (r/atom "")
        loading? (r/atom false)
        error? (r/atom false)]
  (fn []
    [:div {:class "panel panel-primary"}
      [:div {:class "panel-heading"} "Please Login"]
      [:div {:class "panel-body"}
      (alerts/danger error?
        "We are unable to connect you with this password.")
        [:form {:class "form-horizontal form-group col-sm-12"}
          [:div {:class "form-group"}
            [:input (into {:type "password" :id "inputSecretKey" :required ""
                     :class "form-control" :placeholder "Secret key"
                     :on-change #(reset! password (-> % .-target .-value ))
                     :value @password}
                     (when @loading? {:disabled "disabled"}))]]
          [:div {:class "form-group"}
            [:label [:input {:id "inputRemember" :type "checkbox"
                             :checked @remember-me?
                             :on-change #(reset! remember-me?
                               (not @remember-me?))}]
              " Remember me"]]
          [:div {:class "form-group"}
            [:button {:on-click #(auth/login password @remember-me? loading? error?)
                      :type "button"
                      :class (str "btn btn-success btn-block"
                        (when @loading? " disabled"))}
              (if @loading? "Connecting..." "Login")]]]]])))

(defn component []
  [:div {:class "container"}
    [:h1 {:class "page-header"} "Login Page"]
    [login-form]])
