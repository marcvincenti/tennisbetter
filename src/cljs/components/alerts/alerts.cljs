(ns components.alerts)

(defn ^:private close-button [show]
  [:button {:type "button" :class "close" :aria-label "Close"
            :on-click #(reset! show false)}
    [:span {:aria-hidden "true"} "x"]])

(defn success [show msg]
  (if @show
    [:div {:class "alert alert-success" :role "alert"}
      (close-button show)
      [:strong "Well done! "] msg]))

(defn info [show msg]
  (if @show
    [:div {:class "alert alert-info" :role "alert"}
      (close-button show)
      [:strong "Heads up!  "] msg]))

(defn warning [show msg]
  (if @show
    [:div {:class "alert alert-warning" :role "alert"}
      (close-button show)
      [:strong "Warning! "] msg]))

(defn danger [show msg]
  (if @show
    [:div {:class "alert alert-danger" :role "alert"}
      (close-button show)
      [:strong "Oh snap! "] msg]))
