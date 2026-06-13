package lc27bench

import (
	"fmt"
	"math/rand/v2"
	"testing"
)

// --- Solution 1: WriteIndex ---

func writeIndex(nums []int, val int) int {
	writeIdx := 0

	for _, v := range nums {
		if val != v {
			nums[writeIdx] = v
			writeIdx++
		}
	}

	return writeIdx
}

// --- Solution 2: SwapFromEnd ---

func swapFromEnd(nums []int, val int) int {
	n := len(nums)
	i := 0

	for i < n {
		if nums[i] == val {
			nums[i] = nums[n-1]
			n--
		} else {
			i++
		}
	}

	return n
}

// --- Benchmarks ---

var sink int

func benchmarkRemove(b *testing.B, fn func([]int, int) int) {
	for _, n := range []int{100, 1000, 10000} {
		for _, density := range []int{10, 50, 90} {
			b.Run(fmt.Sprintf("n=%d/density=%d", n, density), func(b *testing.B) {
				rng := rand.New(rand.NewPCG(42, uint64(n*1000+density)))
				val := n + density
				nRemove := n * density / 100
				template := make([]int, n)
				for i := range template {
					if i < nRemove {
						template[i] = val
					} else {
						v := rng.IntN(98) + 2
						if v == val {
							v = 1
						}
						template[i] = v
					}
				}
				rand.New(rand.NewPCG(42, uint64(n*1000+density))).Shuffle(len(template), func(i, j int) {
					template[i], template[j] = template[j], template[i]
				})
				buf := make([]int, n)

				b.ResetTimer()
				for b.Loop() {
					copy(buf, template)
					sink = fn(buf, val)
				}
			})
		}
	}
}

func BenchmarkWriteIndex(b *testing.B)  { benchmarkRemove(b, writeIndex) }
func BenchmarkSwapFromEnd(b *testing.B) { benchmarkRemove(b, swapFromEnd) }
