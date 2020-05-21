import org.example.test.api.SpeciesApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Species;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class SpeciesTest {

    SpeciesApi speciesApi = new SpeciesApi();

    @Test
    public void getBonasiaSpecies() throws ApiException {
        Species species = speciesApi.getSpeciesByName("bonasia");
        assertEquals("bonasia", species.getNameScientific());
        assertEquals("Hazel Grouse", species.getNameEnglish());
    }
}
