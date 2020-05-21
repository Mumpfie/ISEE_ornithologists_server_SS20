import org.example.test.api.FamilyApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Family;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class FamilyTest {

    FamilyApi familyApi = new FamilyApi();

    @Test
    public void getCuculidaeFamily() throws ApiException {
        Family family = familyApi.getFamilyByName("Cuculidae");
        assertEquals("Cuculidae", family.getNameScientific());
        assertEquals("Cuckoos", family.getNameEnglish());
    }
}
