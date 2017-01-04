(defproject tennis "0.1.0-SNAPSHOT"
  :description "Tool to help betting on tennis matchs"
  :url "localhost"
  :min-lein-version "2.0.0"
  :source-paths ["src/clj"]
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [org.clojure/clojurescript "1.8.51"]
                 [compojure "1.5.1"]            ;ring wrapper
                 [reagent "0.6.0"]              ;react.js
                 [cljs-http "0.1.42"]           ;ajax calls
                 [secretary "1.2.3"]            ;router for cljs
                 [ring/ring-json "0.5.0-beta1"] ;ring server
                 [org.clojure/data.csv "0.1.3"] ;read csv
                 [amazonica "0.3.79"]]          ;aws java sdk clj wrapper
  :plugins [[lein-ring "0.9.7"]
            [lein-cljsbuild "1.1.4"]]
  :ring {:init server.init/init!
         :handler server.handler/app}
  :cljsbuild {:builds [{:id           "dev"
                        :source-paths ["src/cljs/"]
                        :compiler     {:main app.core
                                       :asset-path "js/out"
                                       :externs    ["externs.js"]
                                       :output-to "resources/public/js/app.js"
                                       :output-dir "resources/public/js/out"}}
                       {:id           "prod"
                        :source-paths ["src/cljs/"]
                        :compiler {:main            app.core
                                   :externs         ["externs.js"]
                                   :output-to       "resources/public/js/app.js"
                                   :optimizations   :advanced
                                   :closure-defines {goog.DEBUG false}
                                   :pretty-print    false}}]})
