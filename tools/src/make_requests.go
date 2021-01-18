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
	target := flag.String("target", "atomic_long_delay",
		"The name of the endpoint to contact, e.g. atomic_long_delay")
	delay := flag.Int("wait", 1,
		"Number of seconds to wait in between requests")
	flag.Parse()

	switch *target {
	case
		"atomic_long_delay",
		"non_atomic_long_delay",
		"atomic_no_delay",
		"non_atomic_no_delay",
		"row_locking_atomic_long_delay":
		*target = fmt.Sprintf("http://localhost/demo/%s/", *target)
	default:
		fmt.Println("Invalid target endpoint.")
		os.Exit(1)
	}
	if *delay < 0 {
		fmt.Println("The delay (wait value) must be positive.")
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
		time.Sleep(time.Second * time.Duration(*delay))
	}

	wt.Wait()
}
