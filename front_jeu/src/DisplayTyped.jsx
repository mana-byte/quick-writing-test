function DisplayTyped({ typedText, fullText, errorText }) {
	const remainingText = fullText.substring(typedText.length);
	const formated_errorText = errorText.replace(" ", "_");
	const isError = errorText !== "";
	let lastChar = !isError ? remainingText[0] : errorText.slice(-1);
	if (lastChar === " ") {
		lastChar = "_";
	}

	return (
		<div>
			{!isError ? (
				<div className="typed-text">
					{typedText}
					<strong className="error-text">{formated_errorText}</strong>
					<strong className="untyped-text">
						<span className="blink">{lastChar}</span>
						{remainingText.slice(1)}
					</strong>
				</div>
			) : (
				<div className="typed-text">
					{typedText}
					<strong className="error-text">
						{formated_errorText.slice(0, -1)}
						<span className="blink">{lastChar}</span>
					</strong>
					<strong className="untyped-text">{remainingText}</strong>
				</div>
			)}
		</div>
	);
}

export default DisplayTyped;
