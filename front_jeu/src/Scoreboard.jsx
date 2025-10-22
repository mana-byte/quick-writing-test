import { cache } from "react";
import TypeWritter from "./TypeWritter";
import ModalForm from "./ModalForm";
import { useState, useEffect } from "react";

function handleDelete(entry) {
  try {
    const rep = fetch(`http://localhost:8000/api/remove_performance/${entry.id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      }
    }).then( (response) => response.json() );
    console.log(rep);
  } catch(error) {
    console.log(error);
  }
}

function handleModify(entry) {

}
function Scoreboard({ scoreBoard }) {
	return (
		<div className="scoreboard">

			{scoreBoard.length > 0 ? (
				<div>
					<h2 className="scoreboard-title">Scoreboard</h2>
					<div className="scoreboard-display">
						{scoreBoard.map((entry, index) => {
							return (
								<div key={index} className="score-entry">
									<TypeWritter text={ (index+1).toString() + " - " + entry.name + " : " + ((entry.time_taken / 1000).toFixed(2)).toString() + " seconds"} speed={100} />
                  <span> 
                    <form>
                      <button className="scoreboard-buttons" onClick={() => { handleDelete(entry) } }> X </button>
                    </form>
                  <ModalForm id={entry.id} name={entry.name} time_taken={entry.time_taken}/>
                  </span>
								</div>
							);
						})}
					</div>
				</div>
			) : (
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
			)}
		</div>
	);
}

export default Scoreboard;
