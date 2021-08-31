package main

import (
    "os"
    "fmt"
    "io/ioutil"
    "net/http"
)

func main(){
    arg := os.Args[1]
    fmt.Println(arg)
    resp, err := http.Get(arg)
    if err != nil {
        fmt.Println(err)
        return
    }
    defer resp.Body.Close()
    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(body))

}
