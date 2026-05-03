async function loadConfig() {
  const response = await fetch('/api/config');
  if (!response.ok) {
    throw new Error('Cannot load app config');
  }
  return response.json();
}

async function loadPositions() {
  const response = await fetch('/data/positions.json');
  if (!response.ok) {
    throw new Error('Cannot load positions');
  }
  return response.json();
}

function createMap(subscriptionKey, positions) {
  const first = positions[0];
  const map = new atlas.Map('map', {
    center: [first.longitude, first.latitude],
    zoom: 12,
    authOptions: {
      authType: 'subscriptionKey',
      subscriptionKey
    }
  });

  map.events.add('ready', () => {
    const dataSource = new atlas.source.DataSource();
    map.sources.add(dataSource);

    for (const point of positions) {
      dataSource.add(new atlas.data.Feature(
        new atlas.data.Point([point.longitude, point.latitude]),
        {
          title: point.device_id,
          description: `${point.timestamp} - ${point.speed_kmh} km/h`
        }
      ));
    }

    map.layers.add(new atlas.layer.SymbolLayer(dataSource, null, {
      iconOptions: { image: 'pin-round-blue' },
      textOptions: {
        textField: ['get', 'title'],
        offset: [0, 1.2]
      }
    }));

    const line = new atlas.data.LineString(
      positions.map(p => [p.longitude, p.latitude])
    );
    dataSource.add(new atlas.data.Feature(line));
    map.layers.add(new atlas.layer.LineLayer(dataSource, null, {
      strokeWidth: 3
    }));
  });
}

(async function main() {
  try {
    const config = await loadConfig();
    const positions = await loadPositions();
    createMap(config.azureMapsKey, positions);
  } catch (error) {
    document.getElementById('map').innerText = error.message;
    console.error(error);
  }
})();
