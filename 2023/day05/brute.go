package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Range struct {
	min int
	max int
}

func (r Range) Contains(x int) bool {
	return x >= r.min && x < r.max
}

func (r Range) Offset(x int) int {
	return x - r.min
}

type Map struct {
	src Range
	dst Range
}

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}

func checkSeed(keys []string, maps map[string][]Map, seed int) int {
	curr := seed
	for _, key := range keys {
		for _, m := range maps[key] {
			if m.src.Contains(curr) {
				offset := m.src.Offset(curr)
				curr = m.dst.min + offset
				break
			}
		}
	}

	return curr
}

func checkRange(keys []string, maps map[string][]Map, min, max int) <-chan int {
	fmt.Printf("%d -> %d\n", min, max)

	c := make(chan int)
	go func() {
		defer close(c)

		best := -1
		for seed := min; seed < max; seed++ {
			curr := checkSeed(keys, maps, seed)
			if best < 0 || curr < best {
				best = curr
			}
		}

		c <- best
	}()

	return c
}

func run() error {
	lines, err := readLines(os.Args[1])
	if err != nil {
		return err
	}

	var seeds []int
	var keys []string

	key := ""
	maps := make(map[string][]Map)
	for _, line := range lines {
		if len(strings.TrimSpace(line)) == 0 {
			continue
		}

		fields := strings.Fields(line)
		if fields[0] == "seeds:" {
			for _, n := range fields[1:] {
				n, err := strconv.Atoi(n)
				if err != nil {
					return err
				}

				seeds = append(seeds, n)
			}
		} else if strings.Contains(line, ":") {
			key = fields[0]
			keys = append(keys, key)
		} else {
			var vals []int
			for _, n := range fields {
				n, err := strconv.Atoi(n)
				if err != nil {
					return err
				}
				vals = append(vals, n)
			}
			m := Map{
				src: Range{
					min: vals[1],
					max: vals[1] + vals[2],
				},
				dst: Range{
					min: vals[0],
					max: vals[0] + vals[2],
				},
			}
			maps[key] = append(maps[key], m)
		}
	}

	// PART 1
	// best := -1
	// for _, seed := range seeds {
	// 	curr := checkSeed(keys, maps, seed)
	// 	if best < 0 || curr < best {
	// 		best = curr
	// 	}
	// }

	// PART 2
	var cs []<-chan int
	for i := 0; i < len(seeds); i += 2 {
		min := seeds[i]
		max := min + seeds[i+1]
		c := checkRange(keys, maps, min, max)
		cs = append(cs, c)
	}

	best := -1
	for _, c := range cs {
		n := <-c
		if best == -1 || n < best {
			best = n
		}
	}

	fmt.Println(best)

	return nil
}

func main() {
	code := 0

	err := run()
	if err != nil {
		fmt.Println(err)
		code = 1
	}

	os.Exit(code)
}
