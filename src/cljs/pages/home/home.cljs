(ns pages.home)

(defn component []
  [:div
    [:div {:class "jumbotron"}
      [:div {:class "container"}
        [:h1 "Tennis bet" [:i "(ter)"]]
        [:p "This project aim to teach us machine learning, data science and
          web development. This application provide advice on how to bet on
          ATP & WTA players."]
        [:p
          [:a {:class "btn btn-primary btn-lg" :href "#/login" :role "button"}
            "Get started »"]]]]
    [:div {:class "container"}
      [:div {:class "row"}
        [:div {:class "col-md-4"}
          [:h2 "Data science"]
          [:p "Donec id elit non mi porta gravida at eget metus.
            Fusce dapibus, tellus ac cursus commodo, tortor mauris
            condimentum nibh, ut fermentum massa justo sit amet
            risus. Etiam porta sem malesuada magna mollis euismod.
            Donec sed odio dui."]
          [:p [:a {:class "btn btn-default" :href "#" :role "button"}
          "View details »"]]]
        [:div {:class "col-md-4"}
          [:h2 "Machine learning"]
          [:p "Donec id elit non mi porta gravida at eget metus.
            Fusce dapibus, tellus ac cursus commodo, tortor mauris
            condimentum nibh, ut fermentum massa justo sit amet
            risus. Etiam porta sem malesuada magna mollis euismod.
            Donec sed odio dui."]
          [:p [:a {:class "btn btn-default" :href "#" :role "button"}
          "View details »"]]]
        [:div {:class "col-md-4"}
          [:h2 "Web dev"]
          [:p "Donec id elit non mi porta gravida at eget metus.
            Fusce dapibus, tellus ac cursus commodo, tortor mauris
            condimentum nibh, ut fermentum massa justo sit amet
            risus. Etiam porta sem malesuada magna mollis euismod.
            Donec sed odio dui."]
          [:p [:a {:class "btn btn-default" :href "#" :role "button"}
          "View details »"]]]]]])
