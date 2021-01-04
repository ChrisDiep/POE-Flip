import { React, useState, useEffect } from 'react'
import { Col, Row, Container, Form, OverlayTrigger, Tooltip, Tab, Nav, Button, Image } from "react-bootstrap"
import axios from 'axios'

import SearchBar from './searchBar'
import dummy from './dummy'

function Selection() {
  const LEAGUES = ["Heist", "Hardcore Heist", "Flashback (DRE007)", "Flashback HC (DRE008)", "Standard", "Hardcore"]
  const [leagues, setLeagues] = useState(LEAGUES)
  const [league, setLeague] = useState(leagues[0])
  const [staticInfo, setStaticInfo] = useState(dummy.static.slice(0, 10))

  // useEffect(() => {

  // }, [])
  return (
    <Container>
      <Row className="justify-content-end">
        <Form className="api-call-switch" inline>
          <Form.Check
            type="switch"
            label="Client-side API Calls"
            id="api-call-switch"
          />
          <OverlayTrigger
            placement="right"
            overlay={
              <Tooltip id="switch-tooltip">
                Gets latest information, but uses your IP to grab the information
              </Tooltip>
            }>
            <span className={'fa fa-question-circle ml-1'}></span>
          </OverlayTrigger>
        </Form>
      </Row>
      <Row>
        <div className="search-container" style={{ "width": "100%" }}>
          <SearchBar leagues={leagues} setLeague={setLeague} league={league} />
        </div>
      </Row>
      <Row>
        <Tab.Container defaultActiveKey={staticInfo[0]["field_id"]} >
          <Row style={{ "width": "100%" }}>
            <Col sm={3}>
              <Nav variant="pills" className="flex-column">
                {staticInfo.map((info) => (
                  <Nav.Item>
                    <Nav.Link eventKey={info["field_id"]}>{info["label"]}</Nav.Link>
                  </Nav.Item>
                ))}
              </Nav>
            </Col>
            <Col sm={9}>
              <Tab.Content>
                {staticInfo.map((info) => (
                  <Tab.Pane eventKey={info["field_id"]}>
                    {info["entries"].map((val) => (
                      <OverlayTrigger
                        overlay={
                          <Tooltip id="currency-tooltip">
                            {val["text"]}
                          </Tooltip>
                        }
                      >
                        <Button variant="outline-dark" style={{ "max-height": "40px", "max-width": "40px", "padding": "4px" }}>
                          <Image style={{ "max-height": "32px", "max-width": "32px" }} src={`https://web.poecdn.com${val["image"]}`}></Image>
                        </Button>
                      </OverlayTrigger>
                    ))}
                    {/* {info["entries"].reduce((acc, val) => acc += val["text"], "")} */}
                  </Tab.Pane>
                ))}
              </Tab.Content>
            </Col>
          </Row>
        </Tab.Container>
      </Row>
    </Container>
  );
}

export default Selection