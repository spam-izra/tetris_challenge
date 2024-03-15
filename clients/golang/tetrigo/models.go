package tetrigo

const (
	Tetramino_O string = "0"
	Tetramino_I string = "1"
	Tetramino_T string = "2"
	Tetramino_L string = "3"
	Tetramino_J string = "4"
	Tetramino_S string = "5"
	Tetramino_Z string = "6"
)

const (
	Orientation_N string = "0"
	Orientation_E string = "1"
	Orientation_S string = "2"
	Orientation_W string = "3"
)

const (
	Command_PASS             = "P"
	Command_SOFT_SPEEDUP     = "S"
	Command_HARD_SPEEDUP     = "H"
	Command_LEFT             = "L"
	Command_RIGHT            = "R"
	Command_CLOCKWISE        = "F"
	Command_COUNTERCLOCKWISE = "B"
)

type Sprite = [][]int

type RotateInfo struct {
	To      string `json:"to"`
	Offsets Sprite
}

type World struct {
	Width              int                                         `json:"width"`
	Height             int                                         `json:"int"`
	Content            Sprite                                      `json:"content"`
	Sprites            map[string]map[string]Sprite                `json:"sprites"`
	SuperRotateSysterm map[string]map[string]map[string]RotateInfo `json:"srs"`
}

type Figure struct {
	X           int     `json:"x"`
	Y           float64 `json:"y"`
	CellY       int     `json:"cell_y"`
	NextY1      float64 `json:"next_y1"`
	NextY2      float64 `json:"next_y2"`
	Figure      string  `json:"figure"`
	Orientation string  `json:"orientation"`
}

type State struct {
	Frame         int      `json:"frame"`
	Score         int      `json:"score"`
	Level         int      `json:"level"`
	Lines         int      `json:"lines"`
	Peek          []string `json:"peek"`
	CurrentFigure *Figure  `json:"current_figure"`
	Speed1        float64  `json:"speed1"`
	Speed2        float64  `json:"speed2"`
	Content       Sprite   `json:"content"`
}

type Commands struct {
	Cmd []string `json:"cmd"`
}
