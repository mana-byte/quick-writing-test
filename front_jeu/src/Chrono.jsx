import { useState, useEffect } from "react";

function Chrono({ isActive, setIsActive, time, setTime }) {
	const [milliseconds, setMilliseconds] = useState(0);
	const [seconds, setSeconds] = useState(0);
	const [minutes, setMinutes] = useState(0);

	useEffect(() => {
		let interval = null;
		if (isActive) {
			interval = setInterval(() => {
        setTime(time + 10);
				setMilliseconds((milliseconds) => milliseconds + 10);
				if (milliseconds >= 1000) {
					setSeconds((seconds) => seconds + 1);
					setMilliseconds(0);
				}
				if (seconds >= 60) {
					setMinutes((minutes) => minutes + 1);
					setSeconds(0);
				}
			}, 10);
		} else if (!isActive && milliseconds !== 0) {
			clearInterval(interval);
			// setMilliseconds(0);
			// setSeconds(0);
			// setMinutes(0);
		}
		return () => clearInterval(interval);
	}, [isActive, milliseconds, seconds, setTime]);

	return (
		<div className="chrono">
			{minutes < 10 ? "0" + minutes : minutes}:
			{seconds < 10 ? "0" + seconds : seconds}:
			{milliseconds < 100
				? milliseconds < 10
					? "00" + milliseconds
					: "0" + milliseconds
				: milliseconds}
		</div>
	);
}

export default Chrono;
