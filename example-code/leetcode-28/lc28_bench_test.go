package lc28bench

import (
	"fmt"
	"math/rand/v2"
	"strings"
	"testing"
)

// --- Solution 1: StringsIndex ---

func strStrLib(haystack string, needle string) int {
	return strings.Index(haystack, needle)
}

// --- Solution 2: ByHand ---

func strStrByHand(haystack string, needle string) int {
	lenH := len(haystack)
	lenN := len(needle)

	for i := 0; i <= lenH-lenN; i++ {
		valid := true
		iCopy := i

		for j := 0; j < lenN && valid; j, iCopy = j+1, iCopy+1 {
			if haystack[iCopy] != needle[j] {
				valid = false
			}
		}

		if valid {
			return i
		}
	}

	return -1
}

// --- Solution 3: Slices ---

func strStrSlice(haystack string, needle string) int {
	for i := 0; i <= len(haystack)-len(needle); i++ {
		if haystack[i:i+len(needle)] == needle {
			return i
		}
	}

	return -1
}

// --- Benchmarks ---

var sink int

const alphabet = "abcdefghijklmnopqrstuvwxyz"

// buildInputs generates a random lowercase haystack and a needle of length
// n*ratio. For "early"/"late" the needle (lowercase) is spliced in;
// for "nomatch" the needle uses uppercase chars that never appear in the haystack.
func buildInputs(n int, ratio float64, scenario string) (string, string) {
	needleLen := max(1, int(float64(n)*ratio))
	rng := rand.New(rand.NewPCG(42, uint64(float64(n)*ratio*1000)))

	buf := make([]byte, n)
	for i := range buf {
		buf[i] = alphabet[rng.IntN(len(alphabet))]
	}

	needle := make([]byte, needleLen)
	if scenario == "nomatch" {
		for i := range needle {
			needle[i] = 'A' // uppercase — never in haystack
		}
	} else {
		for i := range needle {
			needle[i] = alphabet[rng.IntN(len(alphabet))]
		}
		switch scenario {
		case "early":
			copy(buf[:needleLen], needle)
		case "late":
			copy(buf[n-needleLen:], needle)
		}
	}

	return string(buf), string(needle)
}

func benchmarkStrStr(b *testing.B, fn func(string, string) int) {
	for _, n := range []int{100, 1000, 10000} {
		for _, ratio := range []float64{0.01, 0.05, 0.1} {
			for _, scenario := range []string{"early", "late", "nomatch"} {
				haystack, needle := buildInputs(n, ratio, scenario)
				b.Run(fmt.Sprintf("n=%d/ratio=%.2f/%s", n, ratio, scenario), func(b *testing.B) {
					for b.Loop() {
						sink = fn(haystack, needle)
					}
				})
			}
		}
	}
}

func BenchmarkStrStrLib(b *testing.B)    { benchmarkStrStr(b, strStrLib) }
func BenchmarkStrStrByHand(b *testing.B) { benchmarkStrStr(b, strStrByHand) }
func BenchmarkStrStrSlice(b *testing.B)  { benchmarkStrStr(b, strStrSlice) }
