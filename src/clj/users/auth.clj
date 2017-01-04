(ns users.auth
  (:require [ring.util.response :refer [response status]]))

(def ^:private secret-pass "test")  ;passphrase to avoid getting too many users
(def ^:private tokens (atom '()))   ;list of tokens in use

(defn ^:private token
  "Generate a token (string)"
  []
  (.replaceAll (.toString (java.util.UUID/randomUUID)) "-" ""))

(defn login
  "Check if user have the password and return a token"
  [{:keys [password]}]
  (if (= password secret-pass)
    (let [tok (token)]
      (swap! tokens conj tok)
      (response {:token tok}))
    (status (response "Wrong password") 500)))

(defn logout
  "Delete token in tokens vector"
  [{:keys [token]}]
  (swap! tokens #(remove (fn [tok] (= tok token)) %))
  (response "Logged out."))

(defn test-token
  "Check if user is connected"
  [{:keys [token]}]
  (if (some #(= token %) @tokens)
    (response {:token token})
    (status (response "Invalid token") 500)))
