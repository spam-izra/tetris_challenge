package tetrigo

import (
	"encoding/json"
	"errors"
	"os"
	"strconv"
)

func GetWorld() (w World, err error) {
	var msg []byte
	for {
		buffer := make([]byte, 1)
		n, err := os.Stdin.Read(buffer)
		if err != nil {
			return World{}, err
		}
		if n != 1 {
			return World{}, errors.New("cannot Read Byte")
		}

		if buffer[0] != '\n' {
			msg = append(msg, buffer[0])
		} else {
			break
		}
	}

	size, err := strconv.ParseInt(string(msg), 10, 32)
	if err != nil {
		return World{}, err
	}

	body := make([]byte, size)
	os.Stdin.Read(body)
	err = json.Unmarshal(body, &w)
	if err != nil {
		return World{}, err
	}

	return w, nil
}

func GetState() (w State, err error) {
	var msg []byte
	for {
		buffer := make([]byte, 1)
		n, err := os.Stdin.Read(buffer)
		if err != nil {
			return State{}, err
		}
		if n != 1 {
			return State{}, errors.New("cannot Read Byte")
		}

		if buffer[0] != '\n' {
			msg = append(msg, buffer[0])
		} else {
			break
		}
	}

	size, err := strconv.ParseInt(string(msg), 10, 32)
	if err != nil {
		return State{}, err
	}

	body := make([]byte, size)
	os.Stdin.Read(body)
	err = json.Unmarshal(body, &w)
	if err != nil {
		return State{}, err
	}

	return w, nil
}

func SendCmd(cmd []string) error {
	msg := Commands{
		Cmd: cmd,
	}
	body, err := json.Marshal(msg)
	if err != nil {
		return err
	}
	body = append(body, '\n')
	size := strconv.FormatInt(int64(len(body)), 10) + "\n"
	_, err = os.Stdout.Write([]byte(size))
	if err != nil {
		return err
	}
	_, err = os.Stdout.Write(body)
	if err != nil {
		return err
	}

	return nil
}
