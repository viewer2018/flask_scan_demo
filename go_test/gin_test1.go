package main

import "github.com/gin-gonic/gin"
// import "gin-gonic/gin"
import (
    "fmt"
    "io/ioutil"
    "net/http"
	// "gin-gonic/gin"
)

func main() {
    r := gin.Default()
	var url string 

    r.GET("/users/", func(c *gin.Context) {
        // arg := c.Param("arg")
		arg := c.Query("arg")
		fmt.Println(arg)
		resp, err := http.Get(arg)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Println(string(body))	
        c.String(200, "return is %s",string(body))
    })
	r.GET("/h/", func(c *gin.Context) {
        // arg := c.Param("arg")
		arg := c.Query("arg")
		fmt.Println(arg)
		hello := "http://www.baidu.com/"
		url = hello+arg
		resp, err := http.Get(url)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Println(string(body))	
        c.String(200, "return is %s",string(body))
    })
	r.GET("/h1/", func(c *gin.Context) {
        // arg := c.Param("arg")
		arg := c.Query("arg")
		fmt.Println(arg)
		hello := "http://www.baidu.com/"
		url = arg+hello
		resp, err := http.Get(url)
		if err != nil {
			fmt.Println(err)
			return
		}
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Println(string(body))	
        c.String(200, "return is %s",string(body))
    })
    r.Run(":8080")
}