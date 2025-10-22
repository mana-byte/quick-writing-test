import React from 'react';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

function handleModify(entry) {
  try {
    const rep = fetch(`http://localhost:8000/api/update_performance/${entry.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: entry.name, time_taken: entry.time_taken })
    }).then( (response) => response.json() );
    console.log(rep);
  } catch(error) {
    console.log(error);
  }
}

// Make sure to bind modal to your appElement (https://reactcommunity.org/react-modal/accessibility/)
// Bind modal to the app root element for accessibility
// Update this id if your app root element differs (commonly '#root')
Modal.setAppElement('#root');

function ModalForm({ id, name, time_taken}) {
  let subtitle;
  const [modalIsOpen, setIsOpen] = React.useState(false);
  const [newName, setNewName] =  React.useState(name)

  function openModal() {
    setIsOpen(true);
  }

  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    subtitle.style.color = '#f00';
  }

  function closeModal() {
    setIsOpen(false);
  }

  return (
    <div>
      <button className="scoreboard-buttons" onClick={openModal}>Modify</button>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
        <div>Modify the name of {name}</div>
        <form onSubmit={() => {handleModify({id: id, name: newName, time_taken: time_taken})}}>
          <input placeholder='Change name'
            value={newName}
            onChange={(e) => { setNewName(e.target.value) }}/>
          <button>Submit</button>
        </form>
        <div>
          <button onClick={closeModal}>close</button>
        </div>
      </Modal>
    </div>
  );
}

export default ModalForm;
