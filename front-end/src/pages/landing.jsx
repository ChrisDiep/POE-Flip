import { React, useState, useEffect } from 'react';
import { Col, Row, Container, Card, Spinner } from "react-bootstrap";
import Selection from '../components/Selection';
import Listings from '../components/Listings';
import dummy from '../components/dummy';
import axios from 'axios';
import '../App.css';
function Landing() {
  const [listings, setListings] = useState(null)
  const [staticInfo, setStaticInfo] = useState(dummy.static.slice(0, 10))
  const [imagesRef, setImagesRef] = useState(createImagesRef(staticInfo))
  const [loading, setLoading] = useState(false)

  function createImagesRef(data) {
    return dummy.static.slice(0, 10).reduce((acc, category) => {
      category["entries"].forEach((entry) => acc[entry["text"]] = entry["image"])
      return acc;
    }, {})
  }
  function deleteEmptyListings(data) {
    const newData = [];
    for (let index = 0; index < data.length; index += 1) {
      console.log(Object.keys(data[index]["listings"]).length)
      if (Object.keys(data[index]["listings"]).length) {
        newData.push(data[index])
      }
    }
    return newData
  }
  function getListings() {
    setLoading(true);
    axios.get('http://127.0.0.1:5000/api/v1/graph')
      .then((response) => {
        setTimeout(() => {
          setLoading(false);
          setListings(deleteEmptyListings(response.data));
        }, 2000);
      })
      .catch((err) => console.error(err))
    // setListings(dummy.listings)

  }
  return (
    <Card className="landing-card" bg="dark">
      <Card.Body>
        {/* <Container className="landing-container"> */}
        <Row className="justify-content-center selection-row" style={{ "width": "95%" }}>
          <Selection getListings={getListings} staticInfo={staticInfo}></Selection>
        </Row>
        {loading &&
          <Spinner animation="border" role="status">
            <span className="sr-only">Loading...</span>
          </Spinner>}
        {listings
          && <Row className="listings-row" style={{ "margin-top": "10px", "width": "95%" }}>
            <Listings listings={listings} imagesRef={imagesRef}></Listings>
          </Row>}
        {/* </Container> */}
      </Card.Body>
    </Card>
  );
}

export default Landing