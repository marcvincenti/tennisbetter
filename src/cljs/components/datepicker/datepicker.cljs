(ns components.datepicker
  (:require [reagent.core :as r]
            [app.state :refer [app-state]]))

(defn ^:private change-date [ev]
  (swap! app-state assoc-in [:form-p :date] (.val (js/jQuery "#date"))))

(defn ^:private datepicker-render []
  [:input {:class "form-control" :type "text" :id "date"
           :value (or (get-in @app-state [:form-p :date]) "")
           :on-change change-date}])

(defn ^:private datepicker-did-mount [this]
  (.on
    (.datepicker (js/$ (r/dom-node this)) (clj->js {:format "dd/mm/yyyy"}))
    "changeDate" change-date))

(defn datepicker [store]
  (r/create-class {:render datepicker-render
                   :component-did-mount datepicker-did-mount}))
