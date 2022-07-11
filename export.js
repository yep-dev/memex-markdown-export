let len = 0

const keyBy = (array, key) => (array || []).reduce((r, x) => ({ ...r, [key ? x[key] : x]: x }), {});

const getStore = (key, db) => {
  const transaction = db.transaction(key)
  return transaction.objectStore(key)
}

const run = function () {
  const request = indexedDB.open("memex");
  request.onsuccess = async function () {
    const db = request.result;

    let spaces = getStore('customLists', db).getAll();
    let spaceItems = getStore('pageListEntries', db).getAll()
    await new Promise(resolve => {
      setTimeout(resolve, 1000);
    });

    spaces = keyBy(spaces.result, 'id')
    spaceItems = spaceItems.result.reduce((obj, item) => {
      return {
        ...obj,
        [item.pageUrl]: [...obj[item.pageUrl] || [], spaces[item.listId].name],
      };
    }, {});

    const annotations = getStore('annotations', db).getAll();
    annotations.onsuccess = function () {
      if (annotations.result.length !== len) {
        const groupedData = annotations.result.reduce((result, element) => {
          const pageUrl = element.pageUrl
          const id = element.url.substring(element.url.lastIndexOf("#") + 1);
          result[pageUrl] = result[pageUrl] || {
            annotations: [],
            title: element.pageTitle,
            date: new Date(0),
            tags: spaceItems[pageUrl]
          }
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

        len = annotations.result.length
      }

      annotations.oncomplete = function () {
        db.close();
      };
    }
  }
}

run()

setInterval(run, 5 * 1000)
