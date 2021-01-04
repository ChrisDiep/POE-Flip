import React from 'react';
import { InputGroup, FormControl, DropdownButton, Dropdown } from "react-bootstrap";

function searchBar({ leagues, league, setLeague }) {
  return (
    <InputGroup>
      <FormControl
        placeholder="Highlight items"
      />
      <DropdownButton
        as={InputGroup.Append}
        title={league}
      >
        {leagues.map((entry) => (
          <Dropdown.Item
            key={entry}
            onClick={() => (setLeague(entry))}
          >{entry}</Dropdown.Item>
        ))}
      </DropdownButton>
    </InputGroup>
  )
}

export default searchBar;