package main

import (
	"flag"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"sync"
	"time"
)

func main() {
	target := flag.String("endpoint", "ugly", "Either ugly, bad, or good.")
	flag.Parse()

	switch *target {
	case "ugly":
		*target = "http://localhost:80/ugly/"
	case "bad":
		*target = "http://localhost:80/bad/"
	case "good":
		*target = "http://localhost:80/good/"
	default:
		fmt.Println("Invalid endpoint specified. Choose either ugly, bad, or good.")
		os.Exit(1)
	}

	params := url.Values{
		"account": {"1"},
		"amount":  {"100"},
	}

	var wt sync.WaitGroup

	for i := 1; i <= 10; i++ {
		wt.Add(1)
		go func(i int) {
			resp, err := http.PostForm(*target, params)
			if err != nil {
				fmt.Println(err)
			}
			defer resp.Body.Close()

			fmt.Printf("%d: POST %s %d\n", i, *target, resp.StatusCode)
			wt.Done()
		}(i)
		time.Sleep(time.Second)
	}

	wt.Wait()
}
