from filters.keywords import main as filter_keywords
from filters.past_verbs import main as filter_past_verbs
from filters.present_verbs import main as filter_present_verbs
from scrapers.caraguatatuba import main as caraguatatuba_scraper
from scrapers.sao_sebastiao import main as sao_sebastiao_scraper
from scrapers.ubatuba import main as ubatuba_scraper


def execute_pipeline(term: str = "Educação Ambiental"):
    # Step 1: Scraping data
    caraguatatuba_source = caraguatatuba_scraper(term)
    sao_sebastiao_source = sao_sebastiao_scraper(term)
    ubatuba_source = ubatuba_scraper(term)

    # Step 2: Filtering Keywords
    for data_source in (
        ("caraguatatuba", caraguatatuba_source),
        ("ubatuba", ubatuba_source),
        ("sao_sebastiao", sao_sebastiao_source),
    ):
        filter_keywords(data_source[0], data_source[1], False)
        filter_past_verbs(data_source[0], data_source[1], False)
        filter_present_verbs(data_source[0], data_source[1], False)


if __name__ == "__main__":
    execute_pipeline()
