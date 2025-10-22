import { useState, useEffect } from "react";
import DisplayTyped from "./DisplayTyped";

async function handleSubmit(name_, time_taken_) {
	try {
    console.log("works !!!");
		const response = await fetch("http://localhost:8000/api/add_performance", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ name: name_, time_taken: time_taken_ }),
		}).then((rep) => {
			rep.status;
		});
    console.log()
	} catch (error) {
		console.log(error);
	}
}
function FormPerformance({ time_taken, keyStrokes }) {
	// time_taken must be in ms
	const [name, setName] = useState("");
	return (
		<div style={{ textAlign: "center" }}>
			<form
				onSubmit={() => {
					handleSubmit(name, time_taken);
				}}
			>
				<input
					style={{
            opacity: 0,
            left: 0,
            position: "absolute",
            width: '100%',
            height: '100%',
          }}
					onChange={(e) => {
						setName(e.target.value);
					}}
				/>
			</form>
      <DisplayTyped typedText={name} fullText="Enter your Name" errorText="" />
		</div>
	);
}

export default FormPerformance;
