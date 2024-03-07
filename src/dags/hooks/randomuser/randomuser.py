from airflow.providers.http.hooks.http import HttpHook


class RandomUserHook(HttpHook):
    """
    Hook para buscar os dados da API RandomUser
    Documentação: https://randomuser.me/documentation
    """

    default_conn_name = "http_randomuser"
    max_results = 5000

    def __init__(
            self,
            method: str = "GET",
            http_conn_id: str = default_conn_name
    ) -> None:
        super().__init__(method, http_conn_id)
        self._endpoint = "/api"

    def get_user(self, results: int = max_results):
        query = {"results": results}
        return self._get_data(query)

    def get_user_pagination(self, seed: str, max_page: int, results_per_page: int = max_results):
        query = {"seed": seed, "results": results_per_page, "page": 1}

        for page in range(1, max_page + 1):
            query["page"] = page

            yield self._get_data(query)

    def _get_data(self, query: dict):
        results = self._get_max_results(query)
        query["results"] = results

        self.log.info(f"Carregando dados da API {query}")
        response = self.run(endpoint=self._endpoint, data=query)

        return response.json()

    def _get_max_results(self, query: dict):
        results = query.get("results")

        if not results:
            return 1

        if results > self.max_results:
            results = self.max_results

        return results
