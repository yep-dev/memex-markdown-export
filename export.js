let len = 0

setInterval(function () {
  const request = indexedDB.open("memex");
  request.onsuccess = function () {
    const db = request.result;
    const transaction = db.transaction("annotations")
    const store = transaction.objectStore('annotations')

    const query = store.getAll();


    query.onsuccess = function () {
      if (query.result.length !== len) {
        const groupedData = query.result.reduce((result, element) => {
          const pageUrl = element.pageUrl
          const id = element.url.substring(element.url.lastIndexOf("#") + 1);
          result[pageUrl] = result[pageUrl] || { annotations: [], title: element.pageTitle, date: new Date(0) }
          result[pageUrl].date = new Date(result[pageUrl].date).getTime() > element.lastEdited.getTime() ? result[pageUrl].date : element.lastEdited.toISOString().split('T')[0]
          result[pageUrl].annotations.push({
            body: element.body.replace(/\n\n/g, "\nㅤ\n") + "\nㅤ\n",
            comment: element.comment,
            position: element.selector.descriptor.content[1].start,
            url: `https://${element.url}`,
            id,
          })

          return result;
        }, {})


        fetch('http://localhost:8000/load', {
          method: 'POST', headers: {
            'Accept': 'application/json', 'Content-Type': 'application/json'
          }, body: JSON.stringify(groupedData)
        })

        len = query.result.length
      }

      transaction.oncomplete = function () {
        db.close();
      };
    }
  }
}, 5 * 1000);
