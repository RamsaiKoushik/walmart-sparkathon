import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }
    .main {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
    }
    .stButton button {
        background-color: #0071dc;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
        margin-top: 10px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #005bb5;
    }
    .product-card {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .product-card img {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .product-card h3 {
        color: #000;
        font-size: 18px;
        margin: 0;
    }
    .product-card p {
        color: #000;
        font-size: 14px;
    }
    .stars img {
        width: 20px;
        height: 20px;
        margin-right: 2px;
    }
    .product-details {
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-left: 20px; /* Add margin to move content to the right */
    }
    .product-details h1, .product-details h2, .product-details h3, .product-details h4, .product-details h5, .product-details h6, .product-details p {
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Sample product data
products = [
    {
        "name": "Samsung 55\" 4K UHD TV",
        "image_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxASEhAQEBAQDxAQDw8PEA8NDw8NDxAPFREWFhUSFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OGhAQFy0dHR0tLS0tKy0tLy0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tLSstLSstLS0tLS0tKy03Lf/AABEIAMkA+wMBEQACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAAAwQCBQYBB//EAEoQAAEDAgEFCwcHCQkAAAAAAAABAgMEESEFEjFBUQYHExdUYZGSk7TSIjRVcXSBhBQyZIOhsdEWIzVCYnKUs/AkJUNTdaSywcL/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAgMEAQUG/8QANBEBAAICAQIEBAQEBgMAAAAAAAECAxEhEjEEE0FRMjNScRQiI8FCYbHwBTSBgqHhcsLR/9oADAMBAAIRAxEAPwD7iAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA5Ko3wqNj5I1ZUOWOR8blbEitzmOVq2XO0XRSUUtMb07FZntDxu+DSLoiq1+pb4jkxMJeXb2ZLu+pU0w1fYt8Q0eXb2E3fU3+RWdi3xHemTy7eyT8uIOT1nYN8RF3yr+zF27unTTT1ifUN8RzcHlX9njd3lOuinrF+ob4hNoh2MOSe0Pfy6g5PW9g3xHOuvu7+Hy/SzZu1iXRS1y/UM8Zzzae7v4bLH8LP8r2ckruwZ4x5tPdHycn0i7r2cjruwZ4znm09zycn0sXbs4000ld2DPGc87H9TseHyz/CjXdzDyWu7BnjOefj+pL8Jm+iRd3UPJa7sGeMfiMX1O/hM/0Sjdu/p0001b2DPGPPx/U7+C8R9EseMSl5PW9g3xkvOp7ufg8/0Sx4xqXk9b2DfEd82nu5Phc0fwyzbvg0y6KauX6hvjOebT3R/D5fpeu3wKdNNNXdgzxjzae7nk5PpecYNPyau7BnjO+ZT3PIyfScYNPyau7BnjHmV90fKv7POMKm5NXdgzxneuvu50W9mSb4FPyWu7BnjHVHuiyTd5Cuikr+wZ4x1R7u9Ms13bR6fkdf2EfjJ6VzkrHG0a7vYOS13YR+MdMnmU92Lt8KnTTTV3YM8Z3pk8yvu32QMsxVkLaiFHoxz5WZsrcx6OjkcxyKl1/WapFNsQAAAB8HrfOKn2uq/nvNeOPyQ04/hX6NpXeF9V5kV8dSIV9lkVW6Sk125zl78ORXle+TmW1l8VVJ4MbCLIzXcpYaWyaCq19yvrXUM46UqtdbEabCngRCre0L2WmsOwpmWMjMCNpSrKnO0otZfSVV8ZCbL4sjlZgNp1lrZ4idZWbVpIS2JRlGyHmLIsptXa9DZG85GeZU2qgdipZCnpZI07Cq5mlii0CR4nYlRdchhJTZXXG2NNSa1O456pM/5KM6xtkPQrDxZs1UqFkQjNmtr5LIS0lWXa71S/3e32vKHfJTLbvL0a9odecSAAAD4XUtvPU+11X895txfBDTijcL9I3A5aGqkcN3S03kpz4r/wBGK9tSvrVtoKayFE327NYiR8dimZTiVdkF15ha3BELHB6iiZT2kbFYptZGbbTMaIlXMrDIy2OyqbI52FOWdJUlQlQyWu1VYZhDrS6ladp2LbXUlVdGWxK7au+EurYZsp0HWjMIKiyYFlUZhC1pdHLJk4SIhOIZZlmxoV27JWw4jelHduKOlwupRfJviF9Ka5lfbFZLnoeFpqNy8vx2Tc6a+rN1e7x7201cyWLtaRrPVLnMpy3WxxrpR9B3p/0cz2qv75KZbd5b69odgcdAAAD4nIy8tR7XV95kN2L4Ib8Nd0htKGnznImrSvqIZbajbTEcujp4v65jy8k+i7eoX2MwKdqZnlDMmoJ1Gx2QrtJ1MmsKrSTLLNKJ7ubSMadiUJlZahfEcKZVqtxkzzyuxQoOMMzuWqGD3EZlKIVn4nayujhXchprK2EalqTxVJQ6qOS6mivCq8vUYXVYcsss0mzrFNFfE7pRkls6Wl1qZst/SHMdWyhjucw06rLcl+iu0tVgh7OONcPB8RbiZaebSa6108bLfctZXtWykbXbPB03PLmKqNbqciz1JrHo+ib1P6Pb7XlDvkpRbvKcOwOOgAAB8dib5dQv0ut71IbMc/kh6fh/lw32SocL63fcUZp/4Xw3sDDzr93LSmcRiFcK2lfUJhb6Mrlcw4KpVMOlymYEjFEQhKy3QaPRTPdr6l2J52aeWrHHCsplXIXEJWQjcghOEStNNE9sVjLod6kMiai2iz0YJGXwotL1zC2rFk95RJiuBbEM1rttRw6Dl+IZYt1S2MaGOYmZaa8NlSxWS6m/w+Pphh8Tk6p0qZQU34oeT4q2q6ayRpotOqvLrG7aVKyO7TJadvUwflnUOXrWWVRWz04jcO73qv0e32vKHfJTsuOvOAAAAfHqfGSdPplan+6lNeOdU29Pw/y4/v1dVQMw+xPUZMtl7ZsWxjlCXr3YCsOaQ6EE8pvLkJhLTFFKrQ7pkilEuJI1xOxCFuy05cC23FVMRy1kinlZOZbKoXqUysiESqQlNGpKIT7PVQvpDm2Dy6EoYJEW1Sm7NIkTFegvjcqb2hBNEq4rgmw00rEPPzZNlLDjcvrXbBmya4bSIryRyY+IXqZl1QqrTlZa/wCVtHJZDbEaYbTtrakvxyxeJrxtq5V0lma8RGmDw+KZsgfiimTb0YrMS53KceKkYty9PFzV2O9X+j09ryh32UuQnu68OAAAB8gyen52oX6ZXIn8VLc0xP6cPW8NH6Uf36utom4fYYskrZXEUo0g9TE7Dk8IpFxO6dhE5SMwsiWOcZ7J6ZNcUS5MJolFe6uyeodhYlnnVVeOOVB62POtDTEbVnOKJXRCNVI6TiGUbb/iWVqjadM83YX1hHbzM6SyId2zzUT17C+ldo7mWUEN8VNNYZ819cIqhmNi6IYck8ETLGiOIYYjqssQpiVTC7fo29BHrO0hHJPpCzUOwJ7QivDV1Li+k65Zc1erhpqqQzZMk2lo8P4XpqhbMQiyeTD7NZlNulTm+WjBXUOq3rPME9ryh32U1x2UX+KXXHUQAAA+S5Mb5c/ttcifxkv9e4v3+SHseF+TH9+rrIEsieox25lKUtyMwhtmzQciCyKQloiULlIWWVRZxmuuiGbXGeSYWKbE7jjlTk4TVbrDxHZDFG2smeefdsrCEo0setZrXR95OtXJt6QmZjzIWxCueEiJs6Szsj90b5ETBuK7dSFlK7Tiu+7CPTtXaaqw7bs2VOzD1lsQ87NblBNBiW176YrzuET242LkK11CeFmhDjk+zdQNshyZciOVaeTE7WE5hrqx+Cncl9RqEMeLrtv0aGpk0mZ6MUU+GO7SnETrdDm0a4+XU71vmCe2ZR77Mba/DDz8nxz93XEkAAAA+X5EZ5Uy/Ta/vkxOZ/Lp7Hhfkx/fq6BrinTtmaLc4ikaoiCYYPU6Ksryu62iHPMl2mISx4+oyy5bhepXbNCF2GOWXLxzKKvl1FXiZ5TwV42oLiYZauzLNtp07PxIa05vfZ6iXxUnWDeuISsx5kLFc8Er8LJgn2qXVx67la87lVVdSFlYXLdPEbMdeGbLkiG0pGFs108rNbbCtbicp3QiPyqNsSyCeF6ijxucRmNL0r7IQn2SrDWzSFscQ7Mb4aqtnMt7ctuHFqGkq5SMS1RRRdKS270pIpb4A6Xab1/mPxmUe+zG6nww8PN8y33l1pJWAAAHzTJHzZfbco9+mJaev4af0YbRjiMwlpOikHGTHEogljKpGyUQoyvKrLawxYmt3RtMt10fySLL7kMtnYou0j8LmnDGo2yZ450qzOznGHLPVZppHTUvbRp2letO633YXK5hJki616Cda7R/lD1r7+pOg1Y6ExqHkzi2alIe0sV1vqIzMQZL6hfQ24+zDkja5SuxJ3nhitVhXuI0NahUjaWTLla+rY0yWQjMuTHKGrm1EY91la8NbVTWQjkvw04cO5aOqm5zNvb0q49NXO+5OHZhWVTqD1jjqEu+3r/MfjMo99lN9Phh4Ob5lvvLrSSsAAAPmGSn+TKn03KPfpi6sfl29Xw/yobRj/xUhMLdJElIzV3pZRSaw5MMZnlVk6woSyImOsrmFkcoOHvpM94W1hm2TEzzVZttYXWaXRxRjtzdArvcn3mOYaIFUrmBiq29ZHpS7o3P2llYSiqaHRc24qcbU5J509RLqVZLadidQ2UMVkKaTM8yyWtyxVDfS3BPK1SrrJ92XJHKKoddSVXJjhjG0lpBcc/NaVzzJWu2rlk1i06hqpTbV1s5kvbcvSxY9NJO+6natExqFdxZCiyNyBBiw7CEvoG9f5j8ZlHvsxvp8MPBzfMt95daSVAAAB8qyV/je25Q77MaK/DD1vDfKhs76vepFcyVdXSR/m6yY4jLko6iXYU2TrDWTSFUrohC2UqunELVKl1K9I3nhunJZqITvGqstJ3ZAxLmK0NW9M1W2jpOdDkTtWkeQmF9YRMS6k8cblK06hdlXNaejrVXn76rM8nuRTz80SnfhtG4ITx11DNPKNyGikO71CZiWQvmGaZ3O3madiEbWZIh2UI5V66bVsIR7tGOrWVM1kM2S70cOJpaia99hRt6EU1Cm8srKNmLiyGayNx1BiiHYRs7/ev8x+Myj32Y30+GHgZvmW+8usJKgAAA+W5KTCVfpuUe/TGinwvV8PP6UL7Nolelt0qRl1CshCRXncUXWUUJnlS6EESXUhMJTLbUaWsQiOVN+zayaCzJG4Zcc6lFboMs100bYSu2EJhKqk5CuYaYlaoo7rcvwU3O2fxGTUaSV6aENV2fFPO2WTY1RTLeu1l7bhtZFLK0ZolkxLF8RpVa23mdiEZ7JkchLelWtonyWupCZ2spTbU1E2KqQvPo34sbT1s9/wANZjtPL1cePUKKquxegjqVszGu6NVLKqbiNXZ9hdEM1pgVNWsK9sDrku83sPMfjMo99mN9Phh4Gb5lvvLrCSoAAAPlmS1wl9tyj36c00+GHq+H+XC+jgvJJMCMw6qpJiQmEtcIZnlF06qEyla1PRsIWRtLbU7MUORVTa3DYITnlR2QylVqLa2YZuBVNU+rlWcmJnmOWiJ4bSijshvxV1Dzs992YTMupHJZPH2WqdlkuVUruUb2ZquJoiFe+GaKdVTIHJYq4S7EK1ZNZLEGnHVjuamvUtT9h/3Icwz+os8bTXh9/wA4aSV39uX/AFBe8maY/W/3fu9Ov+S/2f8Aq7aBP7bUey0//OU9CPmz9o/d87b/ACtP/K39IcRkKhlSemVYpURJYlVXRvRES6aVsYcFLRaNxL2/GZcc4rxFo7T6w7KlkVtVlJyWu2Klcl9F0jkU3x8Vv9HhXjeHFH85/rDUUG6JlS5sFXBG5sio1r2otmvXRgt1S64XRcPtK65YvxaGjL4WcMdeO08Oay5k1YJ5IrqrWqisculWOS6X59XuKr16baa8OXzKRZ129j5j8ZlHvsxsp8MPGzfMt93WElQAAAfKsl6Juetyj36c00+GHreG+VC80lpejmcRmEoVc7ErlJBPJiU3Sqha26lKyZbKkjO9LPezYtwOaV90kbrkohG0DyFnaiaCvXDszygay7imtN2XWvqrasbZDZrUPMm3VZHm4mW08tUTwnvZCykKpncsWrrLXLPUcd1tXPDNVOTBEoXuOaShp6+p0lOS2o1D0fDYt8yy3JVKfK2XW2c2RqfvK26fcV+Gn9Rd/idJnw069JhIuRKj5cq8E7MWrWfhLfm+DWXPvnaL21abk5w283evXaEeNw/g9dXPTrXrvWnT0siLWVNlvmwQNX95Fev/AKQ0Vn9W32j93kZKzHhab9bT+zQ5L3T1MksLHcHmvexrrMVFsqpe2JRj8Re1oiW/P/h+GmO1o3uI9/8ApuYWqtRlJES6rDTIlsVVeCkNMfFb/R59p/Sxfef6w53c/ufmdLG+SN0Ucb2vVZEViqrVuiIi46UQpx47b3LX4nxNOmYrO5lT3UVbZqh72LdjUaxrk0KjUxVOa6qcyTuzvhqzTHES6Hex8x+Myj32Y1U+GHmZvmW+7qySoAAAPlGTUW02C+e5R1fTpjZjj8kPV8N8uF+yomhceYlpphWmVdi9AmqUQrK5di9BTaEtKsirfWZrQlWFqniXYvQVxVy0tnCxU1L0E9KJSqi7F6FOS7EM477F6CLloFvsXoUjJEMmouxegijKxR06qt7L0Kdx15U5r6jS5Kxdi9Ck8nEM+PujSNdi9CmWI3LTvhjKq7F6FLqwVhG1F2L0KT0W4TNauxehSTNYei7F6FGiFOslzWrdFKrzppw4+qXM1c6qusy2nb28VemEDUXBUuioqKipdFRU0Ki6iHZoiNxy2ybpa1EzeHds+ZHnW/ezb+/SWedk13Y5/wAP8NvfR/zP/wBYZNylNErnRvVHP+eqtR6uxVcc5F2qQre1Z3E93c+DHkiItHEdvT+j2lR7Fa5l0cxUVq2vZU0LiQrOp3COXVqzWe0tgzKtS175EeqPkzEe7g2eVmIqNwtZNKmmuS/fbzsmHFqK64j90FdlmpkarZJXK1dLURrEXmXNRLpzKTm9p9VdcNKzuIax3qt7iK2HY72XmPxmUe+ymyvww8jN8y33dWSVgAAB8yyjvPxSzTTfL6lnDTSzKxrY81qyPVyonNid27uVfiVi9I1XVjG5Nz7vn+6HctweUYsm0U81U9VjZK+TNbmSOW7kTN1NZ5Sr7tSjZufd9A4lYfSFV1Ihs3PucSsPpCq6kRw3Pu94lofSFV1Igbn3e8S8XpCq6sYNz7nEvF6QqurGDc+5xMRekKrqxg3PucTEXpCq6sYNz7veJmL0hVdWMG5epvNR+karqxhzZxNx+karqxgRVG9A5LJFWqqWxdM2TPVb/sORLWDu5TcTkfpCp9zGW91wbk4nI/SFV1Iwbl7xOx+kKrqRhw4nY/SFT1IwHE5Fy+p6kYd3Lzibi5fUdnEDqn3e8TkXL6js4hw71W9zici5dUdnEODqn3OJ2Ll9R2cQ4c6p93vE9Fy+o6kY1B1T7uI3x9yMuTFgfHJJPTy3a+R6Na5siLfMREwxbdUvsUag3Lr8nb1lNPFHPFlCodHKxsjF4OL5rkvjsXmBuVjiei5dUdnEDcu33K5DbQ0zKVsjpUY6R2fIjUcqver1wTD9awcbcAAAAANDu13QtoKWSdbLIv5uBi/rTORc33Jiq8yAcnvR7lpYuGyhWMe2pnc9rEmarZGszrvkcipdHOd9iX/WA+lAAAAAAAAAAAAAAAAAAAAAAAAGr3TZFjraaamkwSRvkutdWSJix6epbevFNYHz/epynPSSvyRWsdE+75KZJEciLZyo9rFVPKYqtc5qpgtnbQPqgAAAAAAAGgyvuXZU1VPUzSPcyl8qKms3guFvfhHLpVfm4fspzgb8AAAAAAAAAAAAAAAAAAAAAAAAAANDuo3MR1vAP4R9PUU0nCQ1ESNV7V1tVF0tuiLbm9YG9T+tQHoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf/9k=",
        "price": "$349.99",
        "description": "Experience stunning picture quality with the Samsung 55\" 4K UHD TV, featuring dynamic crystal color and a sleek design.",
        "rating": 4,
        "category": "Electronics",
        "subcategory": "Television"
    },
    {
        "name": "Apple iPhone 12",
        "image_url": "https://th.bing.com/th/id/OIP.0H_GXDBmj8t95s1KzMU5GAHaL5?w=124&h=199&c=7&r=0&o=5&dpr=1.5&pid=1.7",
        "price": "$799.99",
        "description": "iPhone 12 features 5G speed, A14 Bionic chip, and a Super Retina XDR display for an unmatched mobile experience.",
        "rating": 5,
        "category": "Electronics",
        "subcategory": "Smartphones"
    },
    {
        "name": "Sony WH-1000XM4 Headphones",
        "image_url": "data:image/jpeg;base64,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",
        "price": "$299.99",
        "description": "Sony WH-1000XM4 headphones provide industry-leading noise cancellation, premium sound quality, and all-day comfort.",
        "rating": 4,
        "category": "Electronics",
        "subcategory": "Headphones"
    },
    {
        "name": "Nintendo Switch",
        "image_url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxIREBIQExIQEBASDw8VFRUSEBAVEBAQFhEXFhUSFRUYHSkgGBolHxUWITEiJSkrLi4uFx80ODMsNyotLi0BCgoKDg0OGxAQGCslICUrMjAtLS0tLS0tMDIrLS0tLy0vLi0uLS0vLS0rLSsrLS0rLTUtLTAyKy8tLTctLy8tLv/AABEIALsBDgMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABQIDBAYHAQj/xABDEAABAwIDAwkECAMHBQAAAAABAAIDBBEFEiEGMVEHEyJBYXGBkaEyUrHBFSNCYoKSotEUY/AkM0NTk8LicnOy0uH/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAQMEBQIG/8QALREBAAICAAQEBQMFAAAAAAAAAAECAxEEEiExBUFRYRMicbHwMqHBM1JygZH/2gAMAwEAAhEDEQA/AO4oiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiIIvFcbjgOU3c+17Dge1axWbRSv3HKO8/K3rdRW3UUs1RUQc4WWERYcrSObc02YR1jMCePaoWsqTS07TaSUMLGuLbuky9btb3PnvWa97c3Lt2eGwY4xfEmu+n1/ZsTMZlBvmP4XOafQ6+Kndm9pnyz/wANKASYy+OQWGbKekx7ep2twRoQDutrzDAcYkkjc+UEXkfzeYBjjGG36VzYdfmFW7Gs0cVbASHQzXF+LXEOaew2I7ivEXvTrPZfbh8GeOSI1bW/ePq7uitU04kYyRvsvY1w7nC4+KurY+f7CIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIqXPA1JAHagqRanj/KJh9Hdr5xJIP8ADiu99+BA9nxsub49y1Tvu2lhbC335Tmf+UaDzKDetvabLUQT6ZZI3xHjnH1jSfBr1zQ4jUvqmtMbo4mc5zpJvG9utra9x04dtlThu0c1VG2aaQvkZMA46AZQd9tw6L3bu1bG4LLnnln6w7fh1YyUjcz8s/f1QGITU9TIylcL3j5xrmPN27hlda1jY7ln/RzI6YxMFmhpsFiU9DS073Pa0NNyCWseWjiMwFhbgphkgc24III3jcQqMke2odHhpjWpvFrecxp0Hk4ruew2C/tRB0TuzIbN/Tl81sy5vyRVWV1XSnqeyVo7D0XfBvmukLbindIfO8bj+HntHv8AfqIiKxlEREBERAREQEREBERAREQEREBERAREQEUdi2O01K3PPNHE37z2i54Diexc8x/lop2XbSxPqHe8+8cffqM3p4oOpkqDx3a+iox9fPGx1vZBzSHuYNT4BcBx/lFxCruHTmFhv0ILs/VfN5ELVxG5xJ1uTclx1J4nrKkjr2dgx/lrGraSAn+ZMbDvDBqfEtXOMc2xrqwkS1Ehaf8ADjJZH3ZW6uHfdYEFEPtEnsGgUpT0jR7IA7l5mddmjHw1rd5RtFgcsnUI28Xb/Bo+dlj4xQGCTm75ug117Wvfs7wVulC4DRQe3EfShk4te0+BBHxK8V5ubq15+Ex0wc1e63slLcTRHc5oPxafiFu81U40xkHtGHNpvDsup7xr5Lm+zk2Wob94Ob5i/wAQF0LCX3jLfde8eB6Y9HW8F44jtFvSU+FTu9se+8fn3apiOKOOg6LLWB+yG9VuPcFl7I4kfrBrk5y4B6ib3HwVOL7OMLiW5mgnc0i3hor+EYdzdgBYDqVWbPW9dQ2cD4dkw5ee09I/duGxlZzWLQnc2dj4j4jMP1Nauyr5+qpTEYp2+1FKx472uDh8F36GUPa17dWuaHA8QRcL3w1ukwz+MY9ZK39Y+ytERaXHEREBERAREQEREBERAREQEVEsrWi7iGgcTZaZj3Khh1Ldol/iJBcZYOnqOou9kHsJCDdlj1dbHE0ukexjRvLnAADtXCsf5ZauW7aeNlMzWzj9ZJbj1NaezpLQMQxSoqnZppZZzf7biWg9g9lvgAg7zj3K7QQXbEXVT/5Q6H5z0SO4lc2x/lYr6i7YyylYeqPpSW7XuFvJoK0dsHE+SuBrR1ealCmeaSV2d7pJXne+R7nOP4nG68EXE+X7qtz1lYPhNRWPMdLDJUOFr5AMrQSQC55Ia3cd5G4oMVthuH7q416kNo9la2gDHVMDomPNmvDmPjLrXy5mE2dv0Nr2Nr2Kh2PXuFlJ1KRgcpiDRqhqIXIUtmsFbSnm3Y8kQvRTWKxtpznp79bJGu8Ddv8Au9FbbJqlYc0T28WHztcLxbGstli2Oa+zWaaXI9r/AHXNPkV0jBpOm9vvMa4eBIcfVq5mt4wGpuYH+80sPi3/ANmNWbNG6Sy8Dfk4ik++v+9ElidTI2YNaI+ZyDqBkfIRrrvFjpbdbXvzmMV0he2XPvfm10fUYME45tM2mdzvr5MWvZeN3cur8nlfz2HU7t7mNMZ74zlHoGnxXJMZmyxkdbtB810rkjgczDrnc+olc3uAaz4sKt4afmYPGIicMT7t1REW582IiICIiAiIgIiICIseuqebYXde4d6mI3OoRa0VjcqayubHv1PBQGNbQSMieWWa4C4NhewIvYG/UsGoxBmch0jA/fYvGa2/couuw6IiacNvK+GQZy4us3Jubc2aDYaDettMFYj1lyMnGXmfSPz86OVbfY3UzVUjJZpHR2YQzMRHYtB9gaE3vqVrMUebrsApvblv9qB96Fh9XD5KFpQTcAX3LE666I2jqv3qrNfQLLgwt7t+inaHAmAX6165JU3zVq1sQFHQLYqvDsu7co2SNOVXGWZbVhWzr4WsjgoI8RxB1LHUymosaejjkBMMTYnODXyEC5ud+64vbc9i62+Ltkyhgr8BoqghrQ1oljcGObYbrZiFp20eO1VMKSenmdCavB6RkpaGEvdCXsJuQbEXOosRdSWxlXaXZ6XqczFaN54BpLoW/DyTl6L6230bxyqxx1GD1zGuY90DGyODXNJjdE9shBt7Js0r5qgX0RhPJ/T4bR4nmnklFVTTiV8pa3JCI5N5G82e4lx39i+cqaTQcbBKzpZvScozZX55+pRDJisqN9+9aMV47I+JPZlNeq+cWNdMyu5XqMkwhpG2JHAkeqn8DntDfrikDvAEPt8VC1jeme2x9Fn4BJ0nt4tB8jb5rBaupmEROp3DpN/JYlTiDGdeY8B/Wiidn6CsriYoGukMVmvu4BjBqGk3IGuU+RW9YVySvdY1VQAOtkIue7MbAflK51eGtPd9Nl8Ww0jp1lqOCYfLiNQI2EF3X1siZfV57B6nRd8w2iZBDHCwWZGwNHE26z2nf4rHwPA6ejj5qCMRt3k73vPFzjqSpFa8eKKdnF4rjL8Rrm6aERFYxiIiAiIgIiICIiAoDa6ZzYxlF3BkrgOLmtFh6qfUJtMOjGe1w8wD8lbh/XDPxf8ARt+ebgeL7RSluTpNaNST9p2/NfrcTrfxWx8nOKOkpDG/cHPa3tZlAJ/NmWVtPspDOS9sbWvO/LdodrckgdauYFhXMADTS2gFgBwC14cM1tuZcviuMrlpFaw57ttq6B3WYiPIg/7la2OhD5JQRciNpHg6x+KyttmWEf3JZmev/FWOT939sLfeglHiC13yKyVjV9OrkneKZ9k2+KzlJx6NVrE48rrq2ybRauRg3uFNQ5QdWLFSdRIsDmHSyCNuXM7NbM4Nbo0uN3HQaDrS1NQsomRTx19BSwtqaWnqqN1S0sqpRE2aGWQSNex5BBLbEEd+7S9uqxOnoKWjhbVxVlTS4xFWEUweYhCGAPiExAa4kjq4qKhwyETiKd8hPPSRFlOzPKZWSxta1rd7g8OdawBu3S50TDYnwiGqLIYGU8bnSyPaXOkhqJ30rZzG273Fjg4Zbj2RYam9F4bKJnbDlDrsVjZTRQfwdJUTxw5i5xM7nvLWsdJlADLsdcNB9kgnqOmjBWMZUc7O1s8OXLG0XL7sa8EtflfqHW9m7C05rbjtkODsD5qOJ0mImlhpJ4aaSUUsEsk5MpqIwyQPLY2Tje+95Dc2Cx4MUoqdgidDFJMRi9NM+mme8RwzB3NlhNhPcyloe5x0i7is62WltV5jlXzAvpe2m+193YveZUxbSqYVtmKGdWXAhWHvVsZZ9UakqX3Pgr2Fvyyt7TbzFliAG91ehacwyi5uCO9VzO52tjs7ByOTFlfKy3QlgIJ++0h7AfAy+S7OuB8nGLNixBvS6LmgEjdfOANe5zl3xRKYERFCRERAREQEREBERAREQFDbUf3TT/MH/i5TKiNqB/ZyeD2ept81Zi/XH1UcTG8Vvo5rtcZnQ5acgyBwLmNc0PLPHquoelx/+FZBTThz5/qmvIPsl7gAO2wcPALGbQzUMk1ZI/nWta5rdXdLO4Euffd7IWdgxirg2rfE3nWPe1rrHVoPRK3Rubek/wAORblrT+6vl5TuYaxt0zR/3akn82Y/NQuxcmWvp+10jT4xPHxsth27Z/f/APVC70YFqOBS5KqndwqIfIvAPxWO/TL/ALdXH83Dx/j/AA6PtBotcZWWNlO7SS71pVTJqujEMuGu4TT5wVjRTNE0ZcA9gljLml+QPYHDM0v+yCLi/VdQclcW96xnVriqMuWsdGiuGXSanaKlpJg5tpmuj6UcDqYxwTQyCSjfG+KKNhLSZA6wd0XbydFp2P7XS1L5HBkcQmpI6eVrbua7LPz7pG7spdLd1tbXIUA+UlUiMrHa0T2aKxMd1csj5SC9xeWsjYC43tGxoYxg7A0ADuWfTRWWFHor4je7jbt0HhxVMxMvTPNQxu8jw1KsSYh7rfE/sFTHQ8T5D5n9lKYbgMkzssUL5XcGsc8+Isbd9lMVRqENme/iR2CwHeVcjoid5t3a/wDz1XTcI5Ka2WxkyU7f5jsz7djW39SFu2E8lNHFYyukqHd/Ns8gc36l6S4VTYYXEBrS4ndpck9n9Fbfg/JxXT2+pMTD1y/Vt/KdfJq7vhuEU9OLQwxxdrWjMe928+KzkS5rgPJQ2JzZJpyXNINohYd2d28fhC6UiKAREQEREBERAREQEREBERAUZtK29LJ+A+UjT8lJrAx1t6ab/tPPkL/JeqTq0fVXljeO0e0udzNDgWkAg6EHcQoMmdtU2ONuWmblvlYA0gt1u48D1BTZK8K69q783zNL8u+m+jSduWdKXtp2nxBd+wXPY35XB3uuDvI3+S6XtrHdzfvQyDyP/JcysubxEayS7/BTvBX882549iTXE6rVqmsvoFS5z39RO7crkdC7rsPU+mnqvVuJtMahbjxRWGDkJ3qtkN+JUtBhwJAAc8u3AA9LuA/crb8G5O8QnAy0/MsP2pjzQ8WWzfpWda0OOjceq3fv8hqsiOgHWSfT9/ku1YTyPMFjU1LncWQtDW92Z1yR4BbrhGx1DS2MVNHmH2ngyPvxDn3t4WQcAwTZGqqLGCmkcD9vLlZ/qO09Vu+Fcj07rGeeOEaXawGR/cToAe25XZkRLTcH5M8PgOYxvqH8Znkt/wBNtmnxBW209OyNoaxjWNG5rGhrR4BXUUAiIgIiICIiAiIgIiICIiAiIgIiICIiAqZYw5padQ4EHtBFivbrwuQctrozTyugl6LmnouOjZGfZcD/AFrdY01bG0XL2j8Q+C6bilDBUMyTMbI3qvvb3EahafW8nlI43bNNGOF2HyJC304qNfM4+Xw6ebdOzmu1uItfzZZ0sucEnQdK3j9lQGC7OSVTiKeEykGxsbhvXYg9Xgu5YfslhsGpYJnD7U7s/wCjRvop6PEoY25WZGNG4NDWtHgFmy3i9tw6HDYpxU5ZcqwjkkqX2Mz2Qt4DU+GnyC3bB+TGigsXgzuHW/d5a28LKedjcfvBUHHI+IVTQlKWiiisGMYywtoBe3C+9ZF1AHHmcVSceaoGw3S6136eavRjY4oNhul1AtxgcVcGKjigmrpdQ4xMcVWMQHFBK3S6jhXDiqxWBBnXS6wxVBVCpCDKRY4nCqEyC8itiReh6CtF4CvUHqLxAg9REQEREBeFeogtuarTmrIXlkGG+EFYk2GRO9pgPfdS2VeGNBBOwGn/AMpvqqDs/T/5TfX91P8ANrzmkEAcAg9weZXn0BD7nxWwc0nNINf+govdT6Dj91bDzSc0pGv/AEIzgvfoVnBT/Nr3m1AgPoZvBejCW8FPZF7kQQQwsKoYaFN5EyIIgUCuChUplTKgjhRqoUqkMqWQYIp1WIFl2SyDGESrDFesvUFsNVYC9RB4vURAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERB/9k=",
        "price": "$299.99",
        "description": "Enjoy gaming on the go with the Nintendo Switch, featuring a versatile design that lets you play at home or on the move.",
        "rating": 4,
        "category": "Gaming",
        "subcategory": "Consoles"
    }
]

# Handle query parameters to check if a specific product is selected
query_params = st.experimental_get_query_params()
selected_product = query_params.get("product", None)

if selected_product:
    # Display product details page
    product = next((p for p in products if p["name"] == selected_product[0]), None)
    if product:
        # Use columns with adjusted width to move details further to the right
        col1, col2 = st.columns([1, 3])  # Adjust the column ratio as needed
        
        with col1:
            st.image(product['image_url'], width=300)
        
        with col2:
            st.markdown(f"""
                <div class="product-details">
                    <h1>{product['name']}</h1>
                    <div class='stars'>{''.join(['<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Plain_Yellow_Star.png/1024px-Plain_Yellow_Star.png" alt="star" />' for _ in range(product['rating'])])}</div>
                    <h2>Category: {product['category']}</h2>
                    <h3>Subcategory: {product['subcategory']}</h3>
                    <p>{product['description']}</p>
                    <h2>{product['price']}</h2>
                </div>
            """, unsafe_allow_html=True)

            # "Buy Now" and "Add to Cart" buttons
            col1b, col2b = st.columns(2)
            with col1b:
                st.button('Buy Now', key=f'buy_{product["name"]}')
            with col2b:
                st.button('Add to Cart', key=f'cart_{product["name"]}')
else:
    # Display product listing
    st.title("Recommended Products")

    # Adjust number of columns to display more products per row
    cols = st.columns(4)  # Adjust the number of columns to show more products per row

    for index, product in enumerate(products):
        with cols[index % len(cols)]:
            st.markdown(f"""
                <div class="product-card">
                    <a href="/?product={product['name']}">
                        <img src="{product['image_url']}" alt="{product['name']}" />
                        <h3>{product['name']}</h3>
                        <p>{product['price']}</p>
                    </a>
                </div>
            """, unsafe_allow_html=True)
            st.button('Add to Cart', key=f'button_{index}')