const clean = function () {
  const request = indexedDB.open("memex");
  request.onsuccess = function () {
    const db = request.result;
    const transaction = db.transaction("pages", "readwrite")
    const store = transaction.objectStore('pages')

    const query = store.getAll();

    query.onsuccess = function () {
      const urls = query.result.reduce((result, element) => {
        if (!window.allowed_domains.includes(element.domain)) {
          result.push(element.url)
        }
        return result;
      }, [])


      fetch('http://localhost:8000/log_deleted', {
        method: 'POST', headers: {
          'Accept': 'application/json', 'Content-Type': 'application/json'
        }, body: JSON.stringify(urls )
      }).then(async () => {
        for (let url of urls) {
          const t = db.transaction("pages", "readwrite")
          const x = t.objectStore('pages')
          await x.delete(url)
        }
      })

      transaction.oncomplete = function () {
        db.close();
      };
    }
  }
}
