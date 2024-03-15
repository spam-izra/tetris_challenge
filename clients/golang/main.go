package main

import (
	"math/rand"
	"os"
	"sigillum/tetrigo"
)

type AiBot struct {
}

func (b *AiBot) Update(w *tetrigo.World, s *tetrigo.State) []string {
	poolMove := []string{tetrigo.Command_LEFT, tetrigo.Command_RIGHT, "", "", ""}
	poolRotate := []string{tetrigo.Command_CLOCKWISE, tetrigo.Command_COUNTERCLOCKWISE, "", "", ""}
	poolSpeedUp := []string{tetrigo.Command_SOFT_SPEEDUP, ""}

	cmd := []string{}
	move := poolMove[rand.Intn(len(poolMove))]
	if move != "" {
		cmd = append(cmd, move)
	}
	rotate := poolRotate[rand.Intn(len(poolRotate))]
	if rotate != "" {
		cmd = append(cmd, rotate)
	}

	speedup := poolSpeedUp[rand.Intn(len(poolSpeedUp))]
	if speedup != "" {
		cmd = append(cmd, speedup)
	}

	if len(cmd) == 0 {
		cmd = append(cmd, tetrigo.Command_PASS)
	}

	return cmd
}

func main() {
	old := os.Stderr
	os.Stderr, _ = os.Create("log.txt")
	os.Stderr.WriteString("Hello World\n")

	bot := AiBot{}
	c := tetrigo.Client{}
	c.SetBot(&bot)
	err := c.Loop()

	if err != nil {
		os.Stderr.WriteString("Got err:" + err.Error() + "\n")
	}
	os.Stderr.Close()
	os.Stderr = old
}
