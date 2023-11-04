import { useState, useEffect } from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import Chart from 'react-apexcharts';

export default function Dashboard() {

  const [chartData, setChartData] = useState({});

  useEffect(() => {
    // API call to get chart data
    // setChartData
  }, []);

  return (
    <Row>
      <Col md={6}>
        <Card>
          <Chart 
            options={...}
            series={chartData}
          />
        </Card>
      </Col>

      // ...other components

    </Row>
  )
}