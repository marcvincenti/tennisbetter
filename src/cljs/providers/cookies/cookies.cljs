 (ns providers.cookies
  (:refer-clojure :exclude [get set])
  (:require [reagent.core :as r]
            [cljs.reader :as reader]
            [goog.net.cookies :as cks]))

(defn ^:private read-value [v]
  (when v
    (reader/read-string v)))

(defn get [cookie]
  (->> (name cookie) (.get goog.net.cookies) read-value))

(defn set [cookie content]
    (.set goog.net.cookies (name cookie) (pr-str content)))

(defn remove [cookie]
  (.remove goog.net.cookies (name cookie)))
