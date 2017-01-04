(ns components.datepicker
  (:require [reagent.core :as r]))

(defn ^:private datepicker-render []
  [:input {:class "form-control" :type "text" :id "date"}])

(defn ^:private datepicker-did-mount [this]
  (.datepicker (js/$ (r/dom-node this)) (clj->js {:format "dd/mm/yyyy"})))

(defn datepicker []
  (r/create-class {:render datepicker-render
                   :component-did-mount datepicker-did-mount}))
