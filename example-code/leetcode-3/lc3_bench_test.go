package lc3bench

import (
	"fmt"
	"math/rand/v2"
	"testing"
)

func loopInit(slice []int, val int) {
	for i := range slice {
		slice[i] = val
	}
}

func bulkInit(slice []int, val int) {
	if len(slice) == 0 {
		return
	}
	slice[0] = val
	for bp := 1; bp < len(slice); bp *= 2 {
		copy(slice[bp:], slice[:bp])
	}
}

func TestSolutions(t *testing.T) {
	for _, n := range []int{1000, 10000, 100000} {
		rng := rand.New(rand.NewPCG(42, uint64(n)))
		val := rng.Int()
		s1 := make([]int, n)
		s2 := make([]int, n)
		loopInit(s1, val)
		bulkInit(s2, val)
		for i := range s1 {
			if s1[i] != s2[i] {
				t.Fatalf("n=%d i=%d: loop=%d bulk=%d", n, i, s1[i], s2[i])
			}
		}
	}
}

var sink int

func benchmarkInit(b *testing.B, fn func([]int, int)) {
	for _, n := range []int{1000, 10000, 100000} {
		rng := rand.New(rand.NewPCG(42, uint64(n)))
		val := rng.Int()
		slice := make([]int, n)
		b.Run(fmt.Sprintf("n=%d", n), func(b *testing.B) {
			for b.Loop() {
				fn(slice, val)
				sink = slice[0]
			}
		})
	}
}

func BenchmarkLoopInit(b *testing.B) { benchmarkInit(b, loopInit) }
func BenchmarkBulkInit(b *testing.B) { benchmarkInit(b, bulkInit) }
