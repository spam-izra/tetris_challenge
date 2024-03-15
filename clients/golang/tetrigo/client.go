package tetrigo

type Bot interface {
	Update(w *World, s *State) []string
}

type Client struct {
	bot Bot
}

func (c *Client) SetBot(b Bot) {
	c.bot = b
}

func (c *Client) Loop() error {
	w, err := GetWorld()
	if err != nil {
		return err
	}

	for {
		s, err := GetState()
		if err != nil {
			return err
		}

		cmd := c.bot.Update(&w, &s)
		err = SendCmd(cmd)
		if err != nil {
			return err
		}
	}
}
