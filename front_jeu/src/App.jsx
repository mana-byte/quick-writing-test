import { useState, useEffect } from "react";
import "./App.css";
import Type from "./Type";
import Scoreboard from "./Scoreboard.jsx";

async function fetchScoreBoard() {
	try {
		const rep = await fetch("http://localhost:8000/api/scoreboard").then(
			(res) => res.json(),
		);
		return rep;
	} catch (e) {
		console.error(e);
		return [];
	}
}

function App() {
	const [isPlaying, setIsPlaying] = useState(false);
	const [scoreBoard, setScoreBoard] = useState([]);

	useEffect(() => {
		fetchScoreBoard().then((data) => setScoreBoard(data));
	}, []);
	return (
		<div>
			<div className="background"></div>
			{!isPlaying ? (
				<div>
					<Scoreboard scoreBoard={scoreBoard} />
					<div className="center">
						<button
							type="button"
							className="play-button"
							style={{ fontSize: "2rem", padding: "1rem 2rem" }}
							onClick={() => setIsPlaying((isPlaying) => !isPlaying)}
						>
							{isPlaying ? "Exit" : "Play"}
						</button>
					</div>
				</div>
			) : (
				<div>
					<div className="top-center">
						<button
							type="button"
							className="btn btn-outline-dark"
							onClick={() => setIsPlaying((isPlaying) => !isPlaying)}
						>
							{isPlaying ? "Exit" : "Play"}
						</button>
					</div>
					<Type />
				</div>
			)}
		</div>
	);
}

export default App;
