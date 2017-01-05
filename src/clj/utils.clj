(ns utils)

(defn str->int
  "Converts string to int. Throws an exception if s cannot be parsed as an int"
  [s]
  (if-not (empty? s)
    (Integer/parseInt s)
    0))

(defn str->float
  "Converts string to float. Throws an exception if s cannot be parsed as a
   float"
  [s]
  (Float/parseFloat s))
