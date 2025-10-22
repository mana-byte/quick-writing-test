import { useState, useEffect, useRef } from "react";
import DisplayTyped from "./DisplayTyped.jsx";
import Chrono from "./Chrono.jsx";
import { Mistral } from "@mistralai/mistralai";
import FormPerformance from "./FormPerformance.jsx";

let keyStrokes = 0;

function handleTyping(
  typedTextInForm,
  text,
  setText,
  typedText,
  setTypedText,
  setIsActive,
  isDone,
) {
  if (isDone) return;
  keyStrokes += 1;
  // If the user typed a new character
  if (typedTextInForm.length > typedText.length) {
    const newChar = typedTextInForm.charAt(typedTextInForm.length - 1);
    if (newChar === text.charAt(0) && typedTextInForm === typedText + newChar) {
      setTypedText(typedText + newChar);
      setText(text.substring(1));
    }
  } else if (typedTextInForm.length < typedText.length) {
    const newTypedText = typedText.substring(0, typedTextInForm.length);
    const charsToReturn = typedText.substring(typedTextInForm.length);
    setTypedText(newTypedText);
    setText(charsToReturn + text);
  }

  setIsActive(true);
}

function Type() {
  const inputRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [isDone, setIsDone] = useState(false); // If the user has finished typing the text

  // const apiKey = process.env.MISTRAL_API_KEY;
  // WARNING: REMOVE THE API KEY BEFORE PUSHING TO GITHUB
  const client = new Mistral({ apiKey: "YOUR_API_KEY" }); // Either add it here or in env variables
  const [isLoading, setIsLoading] = useState(false);

  const chatResponse = async (setIsLoading) => {
    setIsLoading(true);
    const response = await client.chat.complete({
      model: "mistral-tiny",
      messages: [
        {
          role: "user",
          content:
            "This is for a writing speed test. Write a short text about a random educative topic. I want only the text, not title or summary or anything else. The text must be around 20 characters long. Also no special characters, only basic punctuation like commas and periods.",
        },
      ],
    });
    setIsLoading(false);
    return response;
  };

  const [text, setText] = useState(""); // Proccessed text to type
  const [fullText, setFullText] = useState(""); // Full text to type (a constant in the program)
  const [typedText, setTypedText] = useState(""); // Text that the user has typed correctly
  const [errorText, setErrorText] = useState(""); // Text that the user has typed incorrectly
  const [typedTextInForm, setTypedTextInForm] = useState(""); // Text that the user has typed in the form
  const [time, setTime] = useState(0); // Time in milliseconds

  // update isDone if typedText equals fullText
  useEffect(() => {
    if (typedText === fullText && fullText.length > 0) {
      setIsDone(true);
      setIsActive(false);
    }
    setErrorText(typedTextInForm.substring(typedText.length));
  }, [
    typedText,
    fullText,
    typedTextInForm,
    setIsDone,
    setIsActive,
    setErrorText,
  ]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
    chatResponse(setIsLoading).then((response) => {
      setText(response.choices[0].message.content);
      setFullText(response.choices[0].message.content);
    });
  }, [setIsLoading, setText, setFullText]);

  return (
    <div className="center">
      <Chrono
        isActive={isActive}
        setIsActive={setIsActive}
        time={time}
        setTime={setTime}
      />
      <div className="info-text">
        <p>
          {fullText.length} characters | {typedText.length} char typed |{" "}
          {keyStrokes} keystrokes
        </p>
      </div>

      {isLoading ? (
        <div className="center" style={{ bottom: "20%" }}>
          <div
            className="spinner-border text-dark"
            role="status"
            style={{
              width: "3rem",
              height: "3rem",
              marginTop: "5rem",
              marginBottom: "2rem",
            }}
          ></div>
        </div>
      ) : (
        <DisplayTyped
          typedText={typedText}
          fullText={fullText}
          errorText={errorText}
        />
      )}
      {isDone ? (
        <div>
          <h2 className="congrats-text">
            Register your name in the scoreboard
          </h2>
          <FormPerformance time_taken={time} keyStrokes={keyStrokes} />
        </div>
      ) : (
        <form className="invisible-form" type="text">
          <input
            ref={inputRef}
            className="invisible-input"
            onChange={(e) => {
              handleTyping(
                e.target.value,
                text,
                setText,
                typedText,
                setTypedText,
                setIsActive,
                isDone,
              );
              setTypedTextInForm(e.target.value);
            }}
            rows="4"
            cols="70"
          />
        </form>
      )}
    </div>
  );
}

export default Type;
